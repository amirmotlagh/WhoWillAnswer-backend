import enum


class GameState(str, enum.Enum):
	WAITING = 'WAITING'
	ACTIVE = 'ACTIVE'
	FINISHED = 'FINISHED'


class UserRoles(str, enum.Enum):
	ADMIN = 'ADMIN'
	MODERATOR = 'MODERATOR'
	USER = 'USER'
