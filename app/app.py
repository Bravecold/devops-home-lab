import os
import time

import psycopg
import redis
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
REQUESTS = Counter("http_requests_total", "HTTP requests", ["path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["path"])


def redis_client():
    return redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)


def db_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        dbname=os.getenv("POSTGRES_DB", "lab"),
        user=os.getenv("POSTGRES_USER", "lab"),
        password=os.getenv("POSTGRES_PASSWORD", "lab-only-change-me"),
        connect_timeout=2,
    )


@app.get("/")
def index():
    start = time.monotonic()
    status = 200
    try:
        visits = redis_client().incr("visits")
        return jsonify(service="devops-lab-api", version=os.getenv("APP_VERSION", "dev"), visits=visits)
    except Exception as exc:
        status = 503
        return jsonify(error="cache unavailable", detail=type(exc).__name__), status
    finally:
        REQUESTS.labels("/", str(status)).inc()
        LATENCY.labels("/").observe(time.monotonic() - start)


@app.get("/health")
def health():
    REQUESTS.labels("/health", "200").inc()
    return jsonify(status="alive")


@app.get("/ready")
def ready():
    try:
        redis_client().ping()
        with db_connection() as conn:
            conn.execute("select 1")
        REQUESTS.labels("/ready", "200").inc()
        return jsonify(status="ready")
    except Exception as exc:
        REQUESTS.labels("/ready", "503").inc()
        return jsonify(status="not-ready", dependency_error=type(exc).__name__), 503


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

