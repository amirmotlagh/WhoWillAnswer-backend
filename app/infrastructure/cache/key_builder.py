class KeyBuilder:
    ROOM = "room"
    GAME = "game"
    @classmethod
    def room_state_key(cls, room_id: str):
        return f"{cls.ROOM}:{room_id}:state"

    @classmethod
    def game_state_key(cls, game_id: str):
        return f"{cls.GAME}:{game_id}:state"
