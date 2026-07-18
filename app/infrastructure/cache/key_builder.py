class KeyBuilder:
	ROOM = 'room'
	GAME = 'game'
	CATEGORY = 'category'

	@classmethod
	def room_state_key(cls, room_id: str):
		return f'{cls.ROOM}:{room_id}:state'

	@classmethod
	def game_state_key(cls, game_id: str):
		return f'{cls.GAME}:{game_id}:state'

	@classmethod
	def game_players_key(cls, game_id: str):
		return f'{cls.GAME}:{game_id}:players'

	@classmethod
	def all_categories_cache_key(cls) -> str:
		return f'{cls.CATEGORY}:all'
