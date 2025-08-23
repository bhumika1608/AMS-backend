
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile

# User details endpoint for authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    serializer = UserSerializer(user)
    # Add is_superuser and is_staff to response
    data = serializer.data
    data['is_superuser'] = user.is_superuser
    data['is_staff'] = user.is_staff
    return Response(data)

@api_view(['POST'])
def register_user(request):
    data = request.data
    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    # Send verification email
    profile = Profile.objects.get(user=user)
    verification_link = f"http://localhost:8000/api/verify-email/{profile.verification_token}/"
    send_mail(
        'Verify your email address',
        f'Click the link to verify your email: {verification_link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
    serializer = UserSerializer(user, many=False)
    return Response({'message': 'Registration successful. Please check your email to verify your account.'}, status=status.HTTP_201_CREATED)
# Email verification endpoint
@api_view(['GET'])
def verify_email(request, token):
    try:
        profile = Profile.objects.get(verification_token=token)
        profile.email_verified = True
        profile.save()
        return Response({'message': 'Email verified successfully.'})
    except Profile.DoesNotExist:
        return Response({'error': 'Invalid verification token.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])
    if user is not None:
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
