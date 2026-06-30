from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import JWTError, jwt

from app.config import settings
from app.schemas.user import TokenData


@dataclass
class TokenInputData:
	user_id: int


def create_access_token(data: TokenInputData, expires_delta: timedelta | None = None) -> str:
	to_encode = asdict(data)
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(minutes=15)
	to_encode.update({'exp': expire, 'type': 'access'})
	encoded_jwt = jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)
	return encoded_jwt


def create_refresh_token(data: TokenInputData, expires_delta: timedelta | None = None) -> str:
	to_encode = asdict(data)
	if expires_delta:
		expire = datetime.now(timezone.utc) + expires_delta
	else:
		expire = datetime.now(timezone.utc) + timedelta(days=7)
	to_encode.update({'exp': expire, 'type': 'refresh'})
	encoded_jwt = jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)
	return encoded_jwt


async def decode_token(token: str) -> TokenData:
	try:
		payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM])
		if payload.get('type') != 'access':
			raise HTTPException(status_code=401, detail='Invalid token type')
		token_data = TokenData(**payload)
		return token_data
	except JWTError as e:
		raise HTTPException(status_code=401, detail=f'Could not validate credentials: {str(e)}')
