From python:3-slim AS build-env

RUN mkdir /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y build-essential \
        python3 libpython3-dev python3-venv

RUN python3 -mvenv /app

RUN pip3 install -U pip setuptools
ADD requirements.txt /app
RUN pip3 install -r requirements.txt -t /app

RUN find /app -name __pycache__ -exec rm -rf -v {} +

ADD main.py /app

FROM gcr.io/distroless/python3-debian10
WORKDIR /app
COPY --from=build-env /app /app
ENV pythonUNBUFFERED=1

ENTRYPOINT ["/usr/bin/python","main.py"]
