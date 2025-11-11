def room_state_key(room_id: str):
    return f"room:{room_id}:state"

def game_state_key(game_id: str) :
    return f"game:{game_id}:state"