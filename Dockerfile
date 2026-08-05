FROM python:3.12-slim
WORKDIR /app
COPY data ./data
COPY tools ./tools
COPY web ./web
ENV PYTHONUNBUFFERED=1 PORT=8080 A3CDB_HOST=0.0.0.0
EXPOSE 8080
CMD ["python", "-m", "tools.a3cdb_query.local_http_server"]
