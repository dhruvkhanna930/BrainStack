from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/login/', views.loginUser, name="login"),
    path('accounts/logout/', views.logoutUser, name="logout"),
    path('accounts/register/', views.registerUser, name="register"),
    path('accounts/forgot-password/', views.forgot_password, name="forgot-password"),
    path('accounts/sendotp/', views.sendotp, name="sendotp"),
    path('accounts/email-verification/', views.email_verification, name="email-verification"),
    path('accounts/reset-password/', views.reset_password, name="reset-password"),

    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.user_profile, name="user-profile"),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<str:pk>', views.update_room, name="update-room"),
    path('delete-room/<str:pk>', views.delete_room, name="delete-room"),
    path('update-message/<str:pk>', views.update_message, name="update-message"),
    path('delete-message/<str:pk>', views.delete_message, name="delete-message"),
    path('update-user/', views.update_user, name="update-user"),
    
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('reactMessage/<str:message_pk>', views.reactMessage, name = "react-message"),
    # path('reactMessage/', views.reactMessage, name = "react-message"),
]