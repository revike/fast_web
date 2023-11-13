from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from backend.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, \
    ALGORITHM

oauth2_scheme = OAuth2PasswordBearer('token')


class OAuth2PasswordRequestBody:

    def __init__(
        self,
        username: str = Body(),
        password: str = Body(),
    ):
        self.username = username
        self.password = password


class Auth:

    @classmethod
    def create_token(cls, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM
        )
        return encoded_jwt

    @classmethod
    async def decode_token(cls, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(
                token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
            phone: str = payload.get("sub")
            token_type: str = payload.get('token_type')
            if token_type == 'access':
                return phone
            error = 'Signature do not has access.'
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)
        except JWTError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'{err}')
