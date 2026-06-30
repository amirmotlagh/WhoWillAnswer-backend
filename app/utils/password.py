from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2', 'bcrypt'], deprecated='auto')


class Hash:
	@staticmethod
	def get_hashed_password(password: str) -> str:
		return pwd_context.hash(password)

	@staticmethod
	def verify(hashed_password: str, plain_password: str) -> bool:
		return pwd_context.verify(plain_password, hashed_password)
