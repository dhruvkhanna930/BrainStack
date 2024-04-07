from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.db.models import Q  #Q for multiple matches when searching

from .models import Room, Topic, Message, User, Likes
from .forms import RoomForm, MessageForm, UserForm, MyUserCreationForm, ChangePasswordForm

import random
from django.conf import settings
from .email import resetPasswordMail

from django.db.models import Count

from django.http import JsonResponse
import google.generativeai as palm
import os
from dotenv import load_dotenv


# Setting up the palmAPIServer
load_dotenv()
try:
    api_key_env = os.environ['CHATBOT_API_KEY']
    palm.configure(api_key=api_key_env)
except KeyError:
    raise ValueError("CHATBOT_API_KEY is not set in the environment variables.")

def chatbot_v2(request):
        message = request.POST.get('message')

        defaults = {
        'model': 'models/chat-bison-001',
        'temperature': 0.25,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
        }
        prompt = message
        context = "Speak like a helper"
        examples = []

        try:
            response = palm.chat(
            **defaults,
            messages=prompt,
            context=context,
            examples=examples,
            )
            return response.last
        except Exception as e:
            # Handle potential errors during chatbot interaction
            return f"Error interacting with the chatbot: {str(e)}"
        

otp = 0


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect('home')

    context = {'page' : page }
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            return redirect('login')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Enter correct password")

        context['user'] = user
    return render(request, 'base/login-register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = "register"

    if request.user.is_authenticated:
        return redirect('home')
    
    form = MyUserCreationForm()

    context = {
        'page' : page,
        'form' : form
    }

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "An error occured during registration")

    return render(request, 'base/login-register.html', context)


# global ForgotPasswordUser = User.objects.get(id = 1)
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            global ForgotPasswordUser
            ForgotPasswordUser = User.objects.get(email=email)
        except:
            messages.error(request, "User with entered email doesn't exist")
            return redirect('forgot-password')

        if ForgotPasswordUser is not None:
            return redirect('sendotp')
    context = {}
    return render(request, 'base/forgot-password.html', context)


def sendotp(request):
    global otp 
    otp = random.randint(100000, 999999)
    to = ForgotPasswordUser.email
    
    print(otp)
    resetPasswordMail(settings.EMAIL_HOST, settings.EMAIL_PORT, settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, to, otp, ForgotPasswordUser.username )
    return redirect('email-verification')


def email_verification(request):
    context = {}
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        try:
            user_otp = int(request.POST.get('otp'))
        except:
            messages.error(request, "Enter valid numeric OTP")
            return redirect('email-verification')

        if user_otp == otp:
            return redirect('reset-password')
        else:
            messages.error(request, "OTP didn't match, enter again")
            return redirect('email-verification')
    return render(request, 'base/email-verification.html', context)


def reset_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            ForgotPasswordUser.set_password(form.cleaned_data['new_password'])
            ForgotPasswordUser.save()
            login(request, ForgotPasswordUser)
            return redirect('login')

    else:
        form = ChangePasswordForm()
    context = {
        'user' : ForgotPasswordUser,
        'form' : form
    }
    return render(request, 'base/reset-password.html', context)


def home(request):
    q = request.GET.get('q')
    # rooms = Room.objects.all()
    if q is not None:
        rooms = Room.objects.filter(
            Q(topic__name__icontains = q) |
            Q(name__icontains = q) |
            Q(description__icontains = q) |
            Q(host__username__icontains = q) |
            Q(host__first_name__icontains = q) |
            Q(host__last_name__icontains = q)
        )  #i here makes it case insensitive
        room_messages = Message.objects.filter(
            Q(room__topic__name__icontains = q)
        )[0:4]

    else:
        rooms = Room.objects.all()
        room_messages = Message.objects.all( )[0:4]
    # topics = Topic.objects.all()[0:5]
    topics = Topic.objects.annotate(num_rooms=Count('room'))
    topics = topics.order_by('-num_rooms')[0:5]
    room_count = rooms.count()  # .count method works faster than the len() method
    
    top_hosts = User.objects.annotate(num_rooms=Count('room__host')).order_by('-num_rooms')[:5]

    total_rooms = Room.objects.all().count()
    # hosts = 

    context = {
        'rooms' : rooms,
        'room_count' : room_count,
        'topics' : topics,
        'room_messages' : room_messages,
        'total_rooms' : total_rooms,
        'top_hosts' : top_hosts
    }

    if request.method == 'POST':
        if request.user.is_authenticated:
            print("Yes")
            response = chatbot_v2(request)
        else:
            print("No")
            response = "Login/SignUp to BrainsStack first to use BrainBot"
        return JsonResponse({'response':response})

    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=int(pk))
    room_messages = room.message_set.all().order_by('-created')  # message model(child) from room model, set of all messages || order by created time descending( - )
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user) #to add new participants who are mesaaging 
        return redirect('room', pk=room.id)  #we are doing this beacuse now a get request is generated instead of POST request(if we dont add redirect) which will mess up some functionalities

    # if request.user in 

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html',context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()[0:5]
    topics = Topic.objects.all()
    total_rooms = Room.objects.all().count()

    context = {
        'user': user,
        'rooms' : rooms,
        'room_messages' : room_messages,
        'topics' : topics,
        'total_rooms' : total_rooms
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    state = 'create'
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)  # if topic exists, it returns that. If it doens't exist then it creates one

        # form = RoomForm(request.POST)
        # # print(request.POST)
        # if form.is_valid():
        #     form.save()

        Room.objects.create(
            host = request.user,
            topic=topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    context = {
        'form' : form,
        'topics' : topics,
        'state' : state
    }
    return render(request, 'base/create.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    state = 'update'
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance = room)  #the form will be pre-filled with the room value because of 'instance' parameter
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
            
        # form = RoomForm(request.POST, instance = room) #if instance not added here then it will create a new form instead of udating

        # if form.is_valid():
        #     form.save()

        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()

        return redirect('home')
    
    context = {
        'form' : form,
        'topics' : topics,
        'room' : room,
        'state' : state
    }
    return render(request, 'base/create.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    type = 'room'
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {
        'obj' : room,
        'type' : type
    }
    return render(request, 'base/delete.html', context)
 

@login_required(login_url='login')
def update_message(request, pk):
    state = 'update'
    message = Message.objects.get(id=pk)
    form = MessageForm(instance = message)  #the form will be pre-filled with the room value because of 'instance' parameter

    if request.user != message.user:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        form = MessageForm(request.POST, instance = message) #if instance not added here then it will create a new form instead of udating
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form' : form,
        'state' : state
    }
    return render(request, 'base/create.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    type = 'message'
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)
    context = {
        'obj' : message,
        'type' : type
    }
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
        # form.username = request.POST.get('username')
        # form.email = request.POST.get('email')
        # form.first_name = request.POST.get('first_nam')
        # form.last_name = request.POST.get('last_name')
      
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {
        'form' : form
    }
    return render(request, 'base/update_user.html', context)


def topicsPage(request):
    q = request.GET.get('q')
    if q is not None:
        topics = Topic.objects.filter(name__icontains=q)
    else:
        # topics = Topic.objects.all()
        topics = Topic.objects.annotate(num_rooms=Count('room'))
        topics = topics.order_by('-num_rooms')
    total_rooms = Room.objects.all().count()
    context = {
        'topics' : topics,
        'total_rooms' : total_rooms
    }
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all( )
    context = {
        'room_messages' : room_messages
    }
    return render(request, 'base/activity.html', context)

@login_required(login_url='login')
def reactMessage(request, message_pk):
    user = request.user
    message = Message.objects.get(id=message_pk)

    if request.method == 'POST':
        if user in message.liked.all():
            message.liked.remove(user)
        else:
            message.liked.add(user)
        
        like, created = Likes.objects.get_or_create(user=user, message=message)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()

    return redirect('room', pk=message.room.id)
         