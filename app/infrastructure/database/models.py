import enum
import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table, Enum, JSON
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.sql import func

from app.infrastructure.database.base import Base


class GameState(str, enum.Enum):
	WAITING = 'WAITING'
	ACTIVE = 'ACTIVE'
	FINISHED = 'FINISHED'


game_players = Table(
	'game_players',
	Base.metadata,
	Column('game_id', Integer, ForeignKey('games.id', ondelete='CASCADE'), primary_key=True),
	Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
)

game_questions = Table(
	'game_questions',
	Base.metadata,
	Column('game_id', Integer, ForeignKey('games.id', ondelete='CASCADE'), primary_key=True),
	Column(
		'question_id', Integer, ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True
	),
)


class User(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
	phone_number: Mapped[str | None] = mapped_column(String(16), unique=True, index=True)
	username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
	full_name: Mapped[str | None] = mapped_column(String(255))
	is_active: Mapped[bool] = mapped_column(default=True)
	created_at: Mapped[datetime.datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now()
	)
	updated_at: Mapped[datetime.datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
	)

	games: Mapped[list['Game']] = relationship(secondary=game_players, back_populates='players')


class Category(Base):
	__tablename__ = 'categories'

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	name: Mapped[str] = mapped_column(String(100), unique=True)
	description: Mapped[str | None] = mapped_column(Text)
	created_at: Mapped[datetime.datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now()
	)
	updated_at: Mapped[datetime.datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
	)

	# Relationship to questions
	questions: Mapped[list['Question']] = relationship(
		back_populates='category', cascade='all, delete-orphan'
	)


class Question(Base):
	__tablename__ = 'questions'

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	text: Mapped[str] = mapped_column(String(255))
	category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
	answers: Mapped[list[str]] = mapped_column(
		MutableList.as_mutable(JSON), nullable=False, default=list, server_default='[]'
	)
	correct_answer: Mapped[int] = mapped_column(Integer, nullable=False)
	approved: Mapped[bool] = mapped_column(default=False, server_default='false')
	created_at: Mapped[datetime.datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now()
	)
	updated_at: Mapped[datetime.datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
	)

	# Relationships
	category: Mapped['Category'] = relationship(back_populates='questions')
	games: Mapped[list['Game']] = relationship(secondary=game_questions, back_populates='questions')

	@validates('answers', 'correct_answer')
	def _validate_answers(self, key, value):
		if key == 'answers':
			if not isinstance(value, list) or len(value) != 4:
				raise ValueError('Answers must be a list with exactly four options.')
		elif key == 'correct_answer':
			if not isinstance(value, int) or value < 0:
				raise ValueError('Correct answer index must be a non-negative integer.')
			if hasattr(self, 'answers') and (value >= len(self.answers)):
				raise ValueError('Correct answer index must be within the range of answers.')
		return value


class Game(Base):
	__tablename__ = 'games'

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	name: Mapped[str] = mapped_column(String(100))
	min_players: Mapped[int]
	max_players: Mapped[int]
	max_timeout: Mapped[int]  # in seconds
	category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
	created_at: Mapped[datetime.datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now()
	)
	updated_at: Mapped[datetime.datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
	)
	started_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))
	ended_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))
	creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
	private: Mapped[bool] = mapped_column(default=False)
	password: Mapped[str | None] = mapped_column(String(100))
	winner: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
	state: Mapped[GameState] = mapped_column(
		Enum(GameState, native_enum=False, length=50), default=GameState.WAITING
	)
	# Relationships
	category: Mapped['Category'] = relationship()
	players: Mapped[list['User']] = relationship(secondary=game_players, back_populates='games')
	questions: Mapped[list['Question']] = relationship(
		secondary=game_questions, back_populates='games'
	)
