FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV TZ=America/Belem

WORKDIR /app

COPY . /app

RUN chmod +x /app/entrypoint.sh \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["./entrypoint.sh"]
