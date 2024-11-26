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

run:
	fastapi dev brain_agriculture/app.py
