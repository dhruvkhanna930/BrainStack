from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def total_hosted_rooms(self):
        return Room.objects.filter(host=self).count()



class Topic(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True) 
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True) #as User is already connected to host, so we add a related_name to connect User to participant
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created', '-updated'] # -created for reverse ordering else it will be in ascending order
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)  #models.CASCADE deletes the messages upon deletion of the Room
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # likes = models.IntegerField(default = 0)
    liked = models.ManyToManyField(User, default=True, blank=True, related_name='liked')

    def __str__(self):
        return self.body[0:50]
    
    @property
    def num_likes(self):
        return self.liked.all().count()
    
    class Meta:
        ordering = ['-created', '-updated']

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_likes')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_likes')
    value = models.CharField(choices = LIKE_CHOICES, default = 'Like', max_length = 10)