from fastapi import FastAPI
from app.core.events.handlers.game_handlers import on_match_created, on_match_started
from app.infrastructure.messaging.subjects import Subjects


async def register_subscribers(app: FastAPI) -> None:
	sub = app.state.subscriber

	await sub.subscribe(
		subject=Subjects.MATCH_CREATED,
		handler=on_match_created,
		durable='match-created-handler',
		queue='game-workers',
		deliver_subject='_deliver.match-created-handler',
	)

	await sub.subscribe(
		subject=Subjects.MATCH_STARTED,
		handler=on_match_started,
		durable='match-started-handler',
		queue='game-workers',
		deliver_subject='_deliver.match-started-handler',
	)
