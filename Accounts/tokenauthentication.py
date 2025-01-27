import jwt, time, os
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    @staticmethod
    def generate_token(payload):
        #here we will generate token based on email which is payload 
        expiration_time = time.time() + (24*3600)
        payload["exp"] = expiration_time
        secret_key = os.getenv("SECRET_KEY")
        
        token = jwt.encode(payload=payload, key=secret_key, algorithm="HS256")
        return token
    
    def authenticate(self, request):
        
        key = os.getenv('SECRET_KEY')
        header = request.headers.get("authorization")
        token = None
        if header and header.startswith("Bearer "):
            token = header.split(" ")[1]

        decoded_token = jwt.decode(token, key = key, algorithms=['HS256'])

        #now we will check expiration 
        expiration = decoded_token.get("exp", None)
        if expiration is None:
            raise AuthenticationFailed("Token expiration is missing")
        
        if time.time() > expiration:
            raise AuthenticationFailed("Token has been expired")
        
        #now we will verify the email and id
        email = decoded_token.get("email", None)
        if email is None:
            raise AuthenticationFailed("Email is missing in token")
        user = User.objects.filter(email=email).first()
        if user:
            return user,None #we are returning a tuple bcoz authentication method which I am overridig expects tuple to be returned
        raise AuthenticationFailed("Email not found")
    
