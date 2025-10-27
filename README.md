# Who Will Answer


# Project Proposal Structure

whowillanswer/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Configuration management (Pydantic Settings)
│   │
│   ├── api/                         # API Layer (HTTP/WebSocket endpoints)
│   │   ├── __init__.py
│   │   ├── dependencies.py          # Shared dependencies (auth, db sessions)
│   │   ├── middleware.py            # Custom middleware (CORS, auth, etc.)
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py          # Login, register, token refresh
│   │   │   │   ├── users.py         # User profile management
│   │   │   │   ├── rooms.py         # Room CRUD operations
│   │   │   │   ├── games.py         # Game management endpoints
│   │   │   │   ├── questions.py     # Question management (admin)
│   │   │   │   └── history.py       # Game history & player stats
│   │   │   └── websockets/
│   │   │       ├── __init__.py
│   │   │       ├── game_ws.py       # Game WebSocket handler
│   │   │       └── room_ws.py       # Room lobby WebSocket handler
│   │
│   ├── core/                        # Core Business Logic (Domain Layer)
│   │   ├── __init__.py
│   │   ├── services/                # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py      # Authentication & JWT handling
│   │   │   ├── user_service.py      # User management
│   │   │   ├── room_service.py      # Room lifecycle management
│   │   │   ├── game_service.py      # Game flow orchestration
│   │   │   ├── gameplay_service.py  # Active game logic (answers, elimination)
│   │   │   ├── question_service.py  # Question retrieval & management
│   │   │   └── history_service.py   # Game history & statistics
│   │   │
│   │   ├── events/                  # Event definitions & handlers
│   │   │   ├── __init__.py
│   │   │   ├── event_bus.py         # Event bus abstraction (NATS wrapper)
│   │   │   ├── event_types.py       # Event type enums/constants
│   │   │   ├── handlers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── room_handlers.py     # ROOM_CREATED, PLAYER_JOINED, etc.
│   │   │   │   ├── game_handlers.py     # GAME_STARTED, GAME_ENDED
│   │   │   │   ├── gameplay_handlers.py # ANSWER_SUBMITTED, PLAYER_ELIMINATED
│   │   │   │   └── timer_handlers.py    # QUESTION_TIMER_EXPIRED
│   │   │   └── subscribers.py       # Event subscriber registration
│   │   │
│   │   ├── domain/                  # Domain models (business entities)
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User domain model
│   │   │   ├── room.py              # Room domain model
│   │   │   ├── game.py              # Game domain model
│   │   │   ├── player_state.py      # Player state in active game
│   │   │   ├── question.py          # Question domain model
│   │   │   └── game_history.py      # Game history domain model
│   │   │
│   │   └── state/                   # State management for active games
│   │       ├── __init__.py
│   │       ├── game_state.py        # In-memory/Redis game state manager
│   │       ├── room_state.py        # Room state manager
│   │       └── timer_manager.py     # Question timer management
│   │
│   ├── infrastructure/              # Infrastructure Layer
│   │   ├── __init__.py
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # SQLAlchemy Base
│   │   │   ├── session.py           # Database session management
│   │   │   ├── models/              # SQLAlchemy ORM models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   ├── room.py
│   │   │   │   ├── game.py
│   │   │   │   ├── question.py
│   │   │   │   ├── game_player.py   # Game participants
│   │   │   │   └── game_answer.py   # Player answers log
│   │   │   └── repositories/        # Data access layer (Repository pattern)
│   │   │       ├── __init__.py
│   │   │       ├── base.py          # Generic repository
│   │   │       ├── user_repository.py
│   │   │       ├── room_repository.py
│   │   │       ├── game_repository.py
│   │   │       ├── question_repository.py
│   │   │       └── history_repository.py
│   │   │
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   ├── redis_client.py      # Redis connection & base operations
│   │   │   ├── game_cache.py        # Active game state in Redis
│   │   │   ├── room_cache.py        # Room state in Redis
│   │   │   └── user_session_cache.py # User sessions/tokens
│   │   │
│   │   ├── messaging/
│   │   │   ├── __init__.py
│   │   │   ├── nats_client.py       # NATS connection management
│   │   │   ├── publisher.py         # Event publisher
│   │   │   ├── subscriber.py        # Event subscriber
│   │   │   └── subjects.py          # NATS subject definitions
│   │   │
│   │   ├── websocket/
│   │   │   ├── __init__.py
│   │   │   ├── connection_manager.py # WebSocket connection pool
│   │   │   ├── broadcaster.py       # Broadcast to specific rooms/users
│   │   │   └── message_handler.py   # WebSocket message routing
│   │   │
│   │   └── security/
│   │       ├── __init__.py
│   │       ├── jwt.py               # JWT token generation & validation
│   │       ├── password.py          # Password hashing (bcrypt)
│   │       └── permissions.py       # Authorization logic
│   │
│   ├── schemas/                     # Pydantic schemas (DTOs)
│   │   ├── __init__.py
│   │   ├── auth.py                  # Login, register requests/responses
│   │   ├── user.py                  # User profile schemas
│   │   ├── room.py                  # Room creation, listing
│   │   ├── game.py                  # Game state schemas
│   │   ├── question.py              # Question schemas
│   │   ├── answer.py                # Answer submission schemas
│   │   ├── history.py               # Game history schemas
│   │   ├── events.py                # Event payload schemas
│   │   └── websocket.py             # WebSocket message schemas
│   │
│   └── utils/                       # Utilities & helpers
│       ├── __init__.py
│       ├── exceptions.py            # Custom exceptions
│       ├── validators.py            # Custom validators
│       ├── enums.py                 # Enums (RoomStatus, GameStatus, etc.)
│       ├── constants.py             # App constants
│       └── logger.py                # Logging configuration
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── unit/
│   │   ├── test_services/
│   │   └── test_domain/
│   ├── integration/
│   │   ├── test_repositories/
│   │   └── test_websockets/
│   └── e2e/
│       └── test_game_flow.py
│
├── alembic/                         # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── scripts/
│   ├── init_db.py                   # Database initialization
│   └── seed_questions.py            # Seed questions for testing
│
├── .env.example
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yml               # Local development setup
├── Dockerfile
├── pyproject.toml                   # Poetry or pip dependencies
├── requirements.txt
└── README.md


# Architucture Diagram
┌─────────────────────────────────────────────────────────────┐
│                     React/TS Frontend                       │
│         (WebSocket + REST API Communication)                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP/WebSocket
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Monolith)                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │              API Layer (REST + WebSocket)               │ │
│ │  ┌──────────┐  ┌────────────┐  ┌──────────────────┐   │ │
│ │  │   Auth   │  │   Rooms    │  │  Game WebSocket  │   │ │
│ │  │  Routes  │  │   Routes   │  │    Connection    │   │ │
│ │  └──────────┘  └────────────┘  └──────────────────┘   │ │
│ └──────────┬─────────────┬───────────────┬───────────────┘ │
│            │             │               │                  │
│            ▼             ▼               ▼                  │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                  Service Layer                          │ │
│ │  ┌──────────┐ ┌────────────┐ ┌─────────────────────┐  │ │
│ │  │   Auth   │ │   Room     │ │     Gameplay        │  │ │
│ │  │  Service │ │  Service   │ │     Service         │  │ │
│ │  └──────────┘ └────────────┘ └─────────────────────┘  │ │
│ │  ┌──────────────────────────────────────────────────┐  │ │
│ │  │         Game State Manager (Redis)               │  │ │
│ │  │  • Active games  • Player states  • Timers      │  │ │
│ │  └──────────────────────────────────────────────────┘  │ │
│ └───────┬──────────────────┬───────────────────┬─────────┘ │
│         │                  │                   │            │
│         ▼                  ▼                   ▼            │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │              Event Bus (NATS Integration)               │ │
│ │                                                          │ │
│ │  Publishers:                    Subscribers:            │ │
│ │  • RoomCreated                 • GameService            │ │
│ │  • PlayerJoined                • WebSocketBroadcaster   │ │
│ │  • GameStarted                 • HistoryService         │ │
│ │  • AnswerSubmitted             • NotificationService    │ │
│ │  • PlayerEliminated            • TimerManager           │ │
│ │  • GameEnded                                            │ │
│ └───────┬──────────────────────────────────┬──────────────┘ │
│         │                                  │                 │
│         ▼                                  ▼                 │
│ ┌──────────────────┐            ┌────────────────────────┐  │
│ │  Repository      │            │  WebSocket Manager     │  │
│ │  Layer           │            │  (Broadcast to rooms)  │  │
│ └────────┬─────────┘            └────────────────────────┘  │
└──────────┼───────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ PostgreSQL   │  │   Redis     │  │       NATS          │ │
│  │              │  │             │  │                     │ │
│  │ • Users      │  │ • Sessions  │  │ • Event streaming   │ │
│  │ • Questions  │  │ • Active    │  │ • Pub/Sub messages  │ │
│  │ • Game       │  │   games     │  │                     │ │
│  │   history    │  │ • Room      │  │                     │ │
│  │              │  │   states    │  │                     │ │
│  └──────────────┘  └─────────────┘  └─────────────────────┘ │
└──────────────────────────────────────────────────────────────┘


# Game Flow Sequence
┌─────────┐     ┌─────────┐     ┌──────────┐     ┌────────┐
│ Player  │     │FastAPI  │     │  Redis   │     │  NATS  │
└────┬────┘     └────┬────┘     └─────┬────┘     └───┬────┘
     │               │                │              │
     │ POST /rooms   │                │              │
     ├──────────────>│                │              │
     │               │ Save room state│              │
     │               ├───────────────>│              │
     │               │ Publish ROOM_CREATED          │
     │               ├──────────────────────────────>│
     │               │                │              │
     │<── 201 Room Created           │              │
     │               │                │              │
     │ WS Connect    │                │              │
     ├──────────────>│                │              │
     │               │ Store WS conn  │              │
     │               ├───────────────>│              │
     │               │                │              │
     │ JOIN_ROOM msg │                │              │
     ├──────────────>│                │              │
     │               │ Update room    │              │
     │               ├───────────────>│              │
     │               │ Publish PLAYER_JOINED         │
     │               ├──────────────────────────────>│
     │               │                │              │
     │               │                │    ┌─────────┴──────┐
     │               │                │    │ Event Handler  │
     │               │                │    │ processes event│
     │               │                │    └─────────┬──────┘
     │               │                │              │
     │               │<─ Broadcast to all players ───┤
     │<── Player joined notification │              │
     │               │                │              │
     │               │ Check if full  │              │
     │               ├───────────────>│              │
     │               │ YES - Start game              │
     │               │ Publish GAME_STARTED          │
     │               ├──────────────────────────────>│
     │               │                │              │
     │               │ Get question   │              │
     │               │ Create timer   │              │
     │               ├───────────────>│              │
     │               │                │              │
     │<── First question broadcast───│              │
     │               │                │              │
     │ SUBMIT_ANSWER │                │              │
     ├──────────────>│                │              │
     │               │ Validate       │              │
     │               ├───────────────>│              │
     │               │ Update state   │              │
     │               ├───────────────>│              │
     │               │ Publish ANSWER_SUBMITTED      │
     │               ├──────────────────────────────>│
     │               │                │              │
     │<── Answer result broadcast────│              │
     │               │                │              │
     │               │ Check mistakes │              │
     │               ├───────────────>│              │
     │               │ 3 mistakes?    │              │
     │               │ Publish PLAYER_ELIMINATED     │
     │               ├──────────────────────────────>│
     │               │                │              │
     │<── Elimination broadcast──────│              │
     │               │                │              │
     │               │ 1 player left? │              │
     │               │ Publish GAME_ENDED            │
     │               ├──────────────────────────────>│
     │               │                │              │
     │               │                │    ┌─────────┴──────┐
     │               │                │    │ Save to        │
     │               │                │    │ PostgreSQL     │
     │               │                │    └─────────┬──────┘
     │               │                │              │
     │               │ Delete from Redis             │
     │               ├───────────────>│              │
     │               │                │              │
     │<── Game results ───────────────│              │
     │               │                │              │
