from enum import StrEnum


class Subjects(StrEnum):
    # Player lifecycle
    PLAYER_JOINED = "game.player.joined"
    PLAYER_LEFT = "game.player.left"
    PLAYER_ACTION = "game.player.action"
    PLAYER_ONLINE = "game.player.online"
    PLAYER_OFFLINE = "game.player.offline"

    # Matchmaking
    PLAYER_MATCHMAKING_REQUESTED = "game.player.matchmaking.requested"

    # Match lifecycle
    MATCH_CREATED = "game.match.created"
    MATCH_STARTED = "game.match.started"
    MATCH_ENDED = "game.match.ended"

    # System
    SYSTEM_HEALTH = "game.system.health"


class SubjectPatterns(StrEnum):
    ALL_GAME = "game.>"
    ALL_PLAYER = "game.player.*"
    ALL_MATCH = "game.match.*"
