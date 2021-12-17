# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1

# When adding a new dependency, run:
# poetry export --without-hashes -f requirements.txt --o django/requirements.txt

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]