.PHONY: lint format run pre_test test post_test

lint:
	ruff check .; \
	ruff check . --diff

format:
	ruff check . --fix; \
	ruff format .

pre_test:
	$(MAKE) lint

test:
	pytest -s -x --cov=brain_agriculture -vv

post_test:
	coverage html

run_postgres:
	docker run -d \
    --name app_database \
    -e POSTGRES_USER=app_user \
    -e POSTGRES_DB=app_db \
    -e POSTGRES_PASSWORD=app_password \
    -v pgdata:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres

run_compose:
	docker-compose up --build