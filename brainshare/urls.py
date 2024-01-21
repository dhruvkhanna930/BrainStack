from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name = 'bs-home'),
    # path('2/', home1, name = 'bs-home1'),
    path('download/<uid>', download),
    path('handle/', HandleFileUpload.as_view())
]