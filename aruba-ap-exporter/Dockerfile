FROM python:3.12-slim-bookworm as builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends gcc

RUN pip install --upgrade pip poetry poetry-plugin-export

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry -C switchinfo export -f requirements.txt --output requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r ./requirements.txt


#########
# FINAL #
#########

FROM python:3.12-slim-bookworm

COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY ./src .

CMD ["python", "./central_clients.py"]
EXPOSE 8000