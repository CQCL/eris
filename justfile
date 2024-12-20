test:
	uv run pytest .

lint:
	uv run ruff format --check
	uv run ruff check

fix:
	uv run ruff format
	uv run ruff check --fix

docs:
	uv run sphinx-apidoc -f -o docs/source/ eris
	uv run sphinx-build -M html docs/source/ docs/build/

build: 
	uv build
