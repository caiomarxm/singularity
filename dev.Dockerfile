FROM python:3.12-alpine as build

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true

RUN poetry install --no-dev


FROM python:3.12-alpine

WORKDIR /app

COPY --from=build /app/.venv /app/.venv

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "singularity.server.server:app", "--host", "0.0.0.0", "--port", "8000"]
