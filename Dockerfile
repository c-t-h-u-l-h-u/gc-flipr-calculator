FROM python:3.9.5 as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.9.5

ARG BF_API_KEY
ENV BF_API_KEY=${BF_API_KEY}

WORKDIR /usr/app

COPY --from=builder /app/wheels /wheels
COPY . .

RUN pip install --no-cache /wheels/*

RUN chown -R 999:999 *

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

USER 999

ENTRYPOINT ["gunicorn",  "--bind", "0.0.0.0:5100", "app:app", "-w"]
CMD ["2"]