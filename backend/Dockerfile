FROM python:3.14 AS builder

WORKDIR /backend

RUN pip install --upgrade pip && \
    pip install uv

COPY requirements.txt ./

RUN uv install

FROM python:3.14 AS final

WORKDIR /backend

COPY --from=builder /backend /backend

COPY . .

RUN uv install