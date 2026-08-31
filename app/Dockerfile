FROM python:3.12-slim AS build
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
ENV PATH="/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 appuser
COPY --from=build /venv /venv
WORKDIR /app
COPY app.py .
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=15s --timeout=3s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')"]
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=2", "--access-logfile=-", "app:app"]

