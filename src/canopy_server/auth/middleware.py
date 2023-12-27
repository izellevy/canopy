from fastapi import Request

import os

from canopy_server.auth.models import TokenPayload
from canopy_server.auth.token_manager import TokenManager

# Get JWT secret from environment variable
jwt_secret = os.environ.get("JWT_SECRET")


def get_current_user(request: Request) -> TokenPayload:
    enable_authorization = jwt_secret is not None

    if not enable_authorization:
        # Authorization is disabled, return a dummy user
        return TokenPayload(sub="dummy_user")

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return TokenManager(jwt_secret).decode_jwt_token(token)


# Custom middleware for authentication
async def authenticate(request: Request, call_next):
    request.state.current_user = get_current_user(request)
    response = await call_next(request)
    return response
