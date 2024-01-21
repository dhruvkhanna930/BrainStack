from django.contrib import admin

from .models import Folder,Files


admin.site.register(Files)
admin.site.register(Folder)

