FROM python:3.14 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /bot

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen --no-dev


FROM python:3.14 AS final

WORKDIR /bot

COPY --from=builder /bot /bot
COPY . .

ENV PATH="/bot/.venv/bin:$PATH"
