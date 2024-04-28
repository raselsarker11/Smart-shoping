from rest_framework.views import APIView
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from .middleware import JwtAuthentication
from django.contrib.auth import authenticate
import jwt




# Generate Token Manually
def get_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user.
    """
    refresh_token = RefreshToken.for_user(user)
    encoded_jwt = jwt.encode({"email": user.email}, "secret", algorithm="HS256")
    return {
        'access': str(encoded_jwt),
        'refresh': str(refresh_token),
    }



# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    

class UserLoginView(APIView):
    authentication_classes = []
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Token generation
            tokens = get_tokens_for_user(user)
            return Response({'access_token': tokens['access'], 'refresh_token': tokens['refresh'], 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            # User authentication failed, return error message
            return Response({'errors': {'non_field_errors': ['Invalid email or password']}}, status=status.HTTP_400_BAD_REQUEST)

    
    
    
    
    

# view for Logout users 
class LogOutAPIView(APIView):
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        

# View for protected endpoint
class MyProtectedView(APIView):
    # authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Access the authenticated user
        user = request.user

        # Perform actions based on the authenticated user
        return Response({"message": f"Hello, {user['username']}! You are authenticated."})



# View for custom token issuance
class CustomTokenIssuanceView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract the refresh token from the request data or headers
            refresh_token = self.get_refresh_token(request)

            # Validate the refresh token (optional)
            self.validate_refresh_token(refresh_token)

            # Create a new access token from the refresh token
            access_token = self.create_access_token(refresh_token)

            # Return the new access token in the response
            return Response({"access_token": str(access_token)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_refresh_token(self, request):
        # Extract the refresh token from the request data or headers
        refresh_token = request.data.get('refresh_token') or request.META.get('HTTP_AUTHORIZATION')

        if not refresh_token:
            raise ValueError("Refresh token not provided")

        return refresh_token

    def validate_refresh_token(self, refresh_token):
        # Validate the refresh token if needed
        token_obj = RefreshToken(refresh_token)

        # Add your validation logic here
        # For example, check if the token is expired, or if it's blacklisted
        if token_obj.is_expired:
            raise ValueError("Refresh token is expired")

        if token_obj.blacklisted:
            raise ValueError("Refresh token is blacklisted")

    def create_access_token(self, refresh_token):
        # Create a new access token from the refresh token
        access_token = RefreshToken(refresh_token).access_token

        return access_token
