# Makefile
.PHONY: migrate

migrate:
	docker exec -u "$$(id -u):$$(id -g)" -it WhoWillAnswer_backend alembic revision --autogenerate -m "$(m)"
