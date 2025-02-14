import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from collections import namedtuple


class UserProxy:
    """A minimal user-like object to store user_id without querying the DB."""

    def __init__(self, user_id):
        self.user_id = user_id
        self.is_authenticated = True  # DRF expects this attribute

    def __str__(self):
        return f"UserProxy(user_id={self.user_id})"


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """Extracts and validates JWT token from the Authorization header."""
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No authentication provided

        token = auth_header.split(" ")[1]  # Extract the token
        
        try:
            payload = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
            user_id = payload.get("user_id")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        # Fetch the user
        # user, _ = User.objects.get_or_create(id=payload["user_id"], username=payload["username"])
        # user = User(id=payload.get("user_id"), username=payload.get("username"), phone_number=payload.get("phone_number"))
        # return (payload, None)  # Required return format: (user, auth)
        return (UserProxy(user_id), None)
