FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN useradd --create-home --uid 10002 ats
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=ats:ats . .
RUN mkdir -p /app/uploads && chown ats:ats /app/uploads
USER ats
EXPOSE 5001
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5001/healthz')"
# Several worker processes so CPU-heavy work (CV parsing in bulk uploads) in one request does not
# slow every other recruiter (one Python process runs one CPU-bound thread at a time).
# Long timeout: bulk uploads still run inside the request until TS-EA-12 moves them to a background job.
ENV ATS_WORKERS=3 ATS_THREADS=6 ATS_TIMEOUT=600
# SQLite mode allows only one process (file lock), so fall back to 1 worker without DATABASE_URL.
CMD ["sh", "-c", "W=${ATS_WORKERS}; [ -z \"$DATABASE_URL\" ] && W=1; exec gunicorn --bind 0.0.0.0:5001 --workers $W --worker-class gthread --threads ${ATS_THREADS} --timeout ${ATS_TIMEOUT} --graceful-timeout 30 --access-logfile - app:app"]
