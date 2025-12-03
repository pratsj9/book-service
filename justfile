dev:
    echo "Starting the app locally on port 8000"
    uv run uvicorn main:app --reload

fmt:
    echo "Performing linting and validation as per the PEP 8 style Guide"
    uv run ruff check
