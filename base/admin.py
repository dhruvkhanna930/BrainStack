from django.contrib import admin

from .models import Room, Topic, Message, User, Likes

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Likes)
