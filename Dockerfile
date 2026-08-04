FROM python:3.12-slim
WORKDIR /app
COPY data ./data
COPY tools ./tools
COPY web ./web
ENV PYTHONUNBUFFERED=1 PORT=8080
EXPOSE 8080
CMD ["python", "-m", "tools.a3cdb_query.public_fixture_server"]
