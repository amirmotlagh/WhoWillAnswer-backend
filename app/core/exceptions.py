class CoreException(Exception):
	"""Base exception for the core application."""

	pass


class UserAlreadyExistsError(CoreException):
	"""Raised when trying to create a user that already exists."""

	pass


class InvalidCredentialsError(CoreException):
	"""Raised when authentication fails due to bad credentials."""

	pass


class InactiveUserError(CoreException):
	"""Raised when a user is inactive."""

	pass


class UserLacksRolesError(CoreException):
	"""Raised when a user has no roles assigned."""

	pass
