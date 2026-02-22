FROM python:3.14 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked --no-dev


FROM python:3.14 AS final

WORKDIR /backend

COPY --from=builder /backend/.venv /backend/.venv
COPY ./__init__.py .
COPY ./src ./src

ENV PATH="/backend/.venv/bin:$PATH"
