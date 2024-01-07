import re
from .models import UserData
from rest_framework_simplejwt.tokens import RefreshToken

def validate_email(email) -> bool:
    return bool(
        bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))
        and not UserData.objects.filter(email=email).exists()
    )


def password_validation(password: str):
    """
    ### password validation

    """
    if len(password) < 6:
        return "Password must be more than 6 chanracter"
    elif not re.search("[a-z]", password):
        return "Password must have atleast one letter"
    elif not re.search("[1-9]", password):
        return "Password must have atleast one number"
    elif not re.search("[~!@#$%^&*]", password):
        return "Password must have atleast one special character"
    elif re.search("[\s]", password):
        return "Space must not be there"
    else:
        return True
    
def validation_name(first_name,last_name:str):
    if not re.search("[a-z]",first_name,last_name):
        raise "name should contains letters"
    elif re.search(["0-9"],first_name,last_name):
        raise "name cannot contains numbers"
    else:
        return True
    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def authenticate_user(request, email: str, password: str) -> str:
    error_msg = "Invalid Credentials"
    pwd_error_msg = "Password is incorrect "
    no_user_error_msg = "User not found "
    user = UserData.objects.filter(email=email).first()
    if not user:
        return False, no_user_error_msg
    if user:
        if user.check_password(password):
            return user, None
        else:
            return False, pwd_error_msg
    return False, error_msg