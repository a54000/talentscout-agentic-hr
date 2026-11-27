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
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5001", "--threads=18", "app:app"]
