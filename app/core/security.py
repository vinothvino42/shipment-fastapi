from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from app.utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/login")


# Method 2 - Custom HTTPBearer to decode and validate JWT access tokens
class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request):
        # Parse Authorization Header
        # Similar to
        # request.header.get("Authorization") ...
        auth_credentials = await super().__call__(request)
        # Access token
        token = auth_credentials.credentials  # type: ignore
        # Validate the token
        token_data = decode_access_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=401,
                detail="Not authorized!",
            )
        # Return token/user data
        return token_data


access_token_bearer = AccessTokenBearer()

# Dependency
AccessTokenDep = Annotated[dict, Depends(access_token_bearer)]
