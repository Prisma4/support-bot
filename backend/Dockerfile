FROM python:3.14 AS builder

WORKDIR /backend

RUN pip install --upgrade pip && \
    pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync

FROM python:3.14 AS final

WORKDIR /backend

COPY --from=builder /backend /backend

COPY . .

RUN uv sync