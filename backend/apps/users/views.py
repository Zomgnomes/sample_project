from datetime import timedelta

from apps.users.models import User
from apps.users.serializers import UserSerializer, UserWriteSerializer
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)

        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return UserSerializer
        return UserWriteSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get("password"))
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if "password" in self.request.data:
            user.set_password(self.request.data.get("password"))
            user.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get_permissions(self):
        """
        Allows login and register methods through without any permissions, otherwise require authentication
        """
        if (
            self.action == "login"
            or self.action == "register"
            or self.action == "password_reset"
            or self.action == "password_change"
        ):
            permissions_classes = [AllowAny]
        else:
            permissions_classes = [IsAuthenticated]
        return [permission() for permission in permissions_classes]

    @action(methods=["GET"], detail=False)
    def profile(self, request):
        if request.user.is_authenticated:
            serializer = self.serializer_class(request.user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=["POST"], detail=False)
    def login(self, request, format=None):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username=email, password=password, request=request)

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                status=status.HTTP_200_OK,
                data={"token": token.key, "user": UserSerializer(user).data},
            )
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["POST"], detail=False)
    def register(self, request):
        last_name = request.data.get("last_name", None)
        first_name = request.data.get("first_name", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if User.objects.filter(email__iexact=email).exists():
            return Response({"status": 210})

        # user creation
        user = User.objects.create(
            email=email,
            password=password,
            last_name=last_name,
            first_name=first_name,
            is_admin=False,
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False)
    def password_reset(self, request, format=None):
        if User.objects.filter(email=request.data["email"]).exists():
            user = User.objects.get(email=request.data["email"])
            user.set_password_reset_token()
            params = {"user": user, "FRONTEND_URL": settings.FRONTEND_URL}
            send_mail(
                subject="Password reset",
                message=render_to_string("mail/password_reset.txt", params),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.data["email"]],
            )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["POST"], detail=False)
    def password_change(self, request, format=None):
        if User.objects.filter(
            password_reset_token=request.data["token"],
            password_token_created_at__gte=timezone.now() - timedelta(minutes=60),
        ).exists():
            user = User.objects.get(password_reset_token=request.data["token"])
            user.clear_password_reset_token()
            # Make sure the password conforms to our password rules here
            user.set_password(request.data["password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
