dev:
    echo "Starting the app locally on port 8000"
    uv run uvicorn main:app --reload

lint:
    echo "Performing linting and validation as per the PEP 8 style Guide"
    uv run ruff check


typecheck:
    echo "TODO//Add basedpyright command here"
