from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify-email'),
    path('user/', views.user_details, name='user-details'),
]
