# base stage
FROM python:3.11.10-slim AS base

ENV PYTHONPATH=/retailcrm_test
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

# final stage
FROM base AS final

COPY /retailcrm_test .

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 8000
