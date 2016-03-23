from passlib.apps import custom_app_context as pwd_context
import os


def check_password(password):
    hashed_password = os.environ.get('AUTH_PASSWORD', 'password failure')
    return pwd_context.verify(password, hashed_password)
