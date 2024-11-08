from flask_server.utils.jwt import verify_jwt   
from typing import Optional


def get_user(jwt: str) -> Optional[str]:
    return verify_jwt(jwt)['user_email']