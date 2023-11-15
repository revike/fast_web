from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from backend.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, \
    ALGORITHM, REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer('token')


class OAuth2PasswordRequestBody:
    def __init__(self, username: str = Body(), password: str = Body()):
        self.username: str = username
        self.password: str = password


class RefreshTokenBody:
    def __init__(self, refresh = Body(default={'refresh': 'refresh_token'})):
        self.refresh = refresh


class Auth:

    @classmethod
    def create_token(cls, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def decode_token(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
            phone: str = payload.get('sub')
            user_id: str = payload.get('user_id')
            token_type: str = payload.get('token_type')
            if token_type == 'access':
                return phone
            elif token_type == 'refresh':
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
                access_token = self.create_token(
                    data={
                        'token_type': 'access',
                        'sub': f'{phone}',
                        'user_id': user_id
                    },
                    expires_delta=access_token_expires,
                )
                refresh_token = self.create_token(
                    data={
                        'token_type': 'refresh',
                        'sub': f'{phone}',
                        'user_id': user_id
                    },
                    expires_delta=refresh_token_expires,
                )
                return {'access': access_token, 'refresh': refresh_token}
            error = 'Signature do not has access.'
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)
        except JWTError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'{err}')
