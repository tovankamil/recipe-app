# --- STAGE 1: BUILDER (Compilation & Installation Stage) ---
# Using stable Python 3.12 Alpine base image.
FROM python:3.12-alpine AS builder

LABEL maintainer="tovan.kamil@gmail.com"

# Set environment for Python output (prevents buffering issues)
ENV PYTHONUNBUFFERED=1

# Install necessary build dependencies (required for compiling C-extensions like psycopg2, even if using binary)
RUN apk add --update --no-cache \
    build-base \
    postgresql-dev \
    musl-dev \
    linux-headers \
    libffi-dev

# Copy requirements files
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
ARG DEV=false

# Install Python packages (using --no-cache-dir to keep layers small)
RUN /usr/local/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
    /usr/local/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; \
    fi && \
    # Cleanup temporary files
    rm -rf /tmp/*

# --- STAGE 2: FINAL (Minimal Runtime Image) ---
FROM python:3.12-alpine

# Install ONLY essential runtime dependencies (libpq for PostgreSQL client)
# postgresql-client is included here for debugging utilities like 'psql'
RUN apk add --update --no-cache \
    postgresql-client \
    libpq

# Setup non-root user for security
RUN adduser \
    --disabled-password \
    --no-create-home \
    --shell /bin/bash \
    django-user

# Set working directory
WORKDIR /app

# Copy compiled packages from the 'builder' stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/flake8 /usr/local/bin/
# Copy application code (owned by django-user)
COPY --chown=django-user:django-user . /app

# Ensure application user has access rights
RUN chown -R django-user:django-user /app

# Switch to non-root user
USER django-user

EXPOSE 8000

# Default command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
