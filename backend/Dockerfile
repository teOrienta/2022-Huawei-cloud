FROM python:3.10-bullseye AS build-stage

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.10-bullseye AS runtime-stage
WORKDIR /usr/app/backend

COPY --from=build-stage /opt/venv /opt/venv

RUN apt-get -y update && \
    apt-get -y install sudo && \
    sudo apt-get -y install graphviz
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000