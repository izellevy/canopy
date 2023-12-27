import jwt

from datetime import datetime, timedelta
import os

from jwt import PyJWTError
import secrets

from canopy_server.auth.models import TokenPayload

# Get JWT secret from environment variable
jwt_secret = os.environ.get("JWT_SECRET")


class TokenManager:
    def __init__(self, jwt_secret: str, algorithm="HS256"):
        self._jwt_secret = jwt_secret
        self._algorithm = algorithm

    @classmethod
    def _get_expiration_timestamp(cls, expires_delta: timedelta = None):
        # Add expiration time if provided
        if expires_delta is not None:
            expiry_date = datetime.utcnow() + expires_delta
            return int(expiry_date.timestamp())
        else:
            return None

    def create_jwt_token(self, subject: str, expires_delta: timedelta = None) -> str:
        payload = TokenPayload(sub=subject, exp=self._get_expiration_timestamp(expires_delta))
        to_encode = payload.dict(exclude_none=True)
        return jwt.encode(to_encode, self._jwt_secret, algorithm=self._algorithm)

    def decode_jwt_token(self, token: str):
        try:
            payload = jwt.decode(token, self._jwt_secret, algorithms=[self._algorithm])
            return TokenPayload(**payload)
        except jwt.ExpiredSignatureError:
            return TokenPayload(sub="expired_user")
        except PyJWTError:
            # Handle JWTError in a more general way
            return TokenPayload(sub="invalid_user")

    @staticmethod
    def generate_jwt_secret() -> str:
        return secrets.token_hex(32)


if __name__ == '__main__':
    secret = TokenManager.generate_jwt_secret()
    token_manager = TokenManager(secret)

    print(secret)
    tkn = token_manager.create_jwt_token("izel", expires_delta=timedelta(microseconds=0))
    print(token_manager.decode_jwt_token(tkn))
