FROM ubuntu:19.10

COPY ./app /api/app
COPY requirements.txt /requirements.txt

RUN apt-get update \
    && apt-get install python3-dev python3-pip -y \
    && pip3 install -r requirements.txt

ENV PYTHONPATH=/app
WORKDIR /app

EXPOSE $PORT

# ENTRYPOINT ["uvicorn"]
# CMD ["api.main:app", "--host", "0.0.0.0"]