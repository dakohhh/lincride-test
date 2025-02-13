from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from app.common.exceptions import BadRequestException
from app.user.models import User
from app.user.serializers import UserPublicSerializers
from app.common.response import CustomResponse as Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, RequestTokenSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        tags=["Authentication"],
        responses={200: None}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(
        tags=["Authentication"],
        responses={200: None}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SignupAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


    def create(self, request):

        # Check if the user already exists
        is_user_exist = User.objects.filter(email=request.data["email"]).exists()

        if is_user_exist:
            raise BadRequestException("User with this email already exists")

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        # Get the access and refresh token
        tokens = self.get_tokens(instance)

        # Add the tokens to the user data
        result = {
            "user": UserPublicSerializers(instance).data,
            "tokens": tokens
        }

        return result
    

    def get_tokens(self, user):
        """Generates access and refresh tokens for the created user"""

        refresh = RefreshToken.for_user(user)

        tokens = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
        
        return tokens
    
    @extend_schema(
        summary="Registers Users",
        tags=["Authentication"],
        auth=[],
        request=RegisterSerializer,
        responses={201: UserPublicSerializers}
    )
    def post(self, request: Request):
        result = self.create(request)
        return Response("Signup Successfully", result)


class SessionAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPublicSerializers


    @extend_schema(
        tags=["Authentication"],
        responses={200: UserPublicSerializers}
    )
    def get(self, request: Request):
        serializer_class = UserPublicSerializers(request.user)
        return Response("Get session info for user", serializer_class.data)


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout a user",
        tags=["Authentication"],
        request=RequestTokenSerializer,
        responses={204: None}
    )
    def post(self, request: Request):

        refresh_token_serializer = RequestTokenSerializer(data=request.data)

        # Validate the input
        if not refresh_token_serializer.is_valid():
            raise BadRequestException(refresh_token_serializer.errors)

        refresh_token = RefreshToken(refresh_token_serializer.validated_data["refresh"])

        refresh_token.blacklist()

        return Response("Logout Successfully", status_code=status.HTTP_204_NO_CONTENT)
