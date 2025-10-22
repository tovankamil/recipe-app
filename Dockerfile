FROM python:3.15.0a1-alpine3.21
LABEL maintainer="tovan.kamil@gmail.com"

ENV PYTHONUNBUFFERED=1

# Salin requirements.txt dan tetapkan ARG
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
ARG DEV=false

# Layer RUN tunggal untuk instalasi, pembersihan cache, dan pembuatan venv
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # PERBAIKAN SINTAKS SHELL KRITIS DI SINI
    if [ "$DEV" = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp/requirements.txt && \
    rm -rf /tmp/requirements.dev.txt && \ 
    rm -rf /root/.cache/pip

# Buat user non-root DAN alihkan kepemilikan /py dalam satu layer RUN.
RUN adduser -D -H -S django-user && \
    chown -R django-user /py

# Atur PATH VENV
ENV PATH="/py/bin:$PATH"

# Atur workdir dan Salin kode aplikasi
WORKDIR /app
COPY . /app

# Beralih ke user non-root untuk menjalankan aplikasi
USER django-user

EXPOSE 8000