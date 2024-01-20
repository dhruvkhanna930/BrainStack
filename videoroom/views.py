from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from agora_token_builder import RtcTokenBuilder

from .models import RoomMember

import random
import time

import os
from dotenv import load_dotenv

load_dotenv()

def getToken(request):
    appId = '9a90c4b3fdc44f44be55f81ec694509b'
    appCertificate = os.environ['AGORA_APP_CERTIFICATE']
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1


    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token':token, 'uid':uid, 'currentUser':request.user.username}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False) 


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)
 

def lobby(request):
    navbar = False
    context = {
        'navbar': navbar,
    }
    return render(request, 'videoroom/lobby.html', context)

def room(request):
    navbar = False
    context = {
        'navbar': navbar,
    }
    return render(request, 'videoroom/room.html', context)
