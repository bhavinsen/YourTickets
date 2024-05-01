FROM python:3.10-alpine as base
RUN apk update 
RUN apk add curl openssl-dev npm nodejs


ADD yt_dashboard/package*.json /tmp/
RUN cd /tmp && NODE_OPTIONS=--openssl-legacy-provider npm install

COPY ./yt_dashboard /app/yt_dashboard
WORKDIR /app/

RUN cd yt_dashboard && \
    #NODE_OPTIONS=--openssl-legacy-provider npm install && \
    cp -a /tmp/node_modules . && \
    NODE_OPTIONS=--openssl-legacy-provider npm run build && \
    npm cache clean --force


FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG ENVIRONMENT

ENV DB_NAME=$DB_NAME
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV ENVIRONMENT=$ENVIRONMENT

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

# RUN apk update \
#     # && apk add --virtual  \
#     && apk add --no-cache build-deps gcc python3-dev musl-dev xvfb musl-dev libffi-dev openssl-dev curl \
#     zlib-dev jpeg-dev bash wkhtmltopdf freetype-dev libjpeg-turbo-dev libpng-dev \
#     && pip install --no-cache-dir -r requirements.txt \
#     && rm -rf /var/lib/apt/lists/* \
#     && apk del build-deps

# gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN apk update && apk add --no-cache gcc xvfb musl-dev libffi-dev openssl-dev \
    zlib-dev jpeg-dev bash wkhtmltopdf curl build-base freetype-dev libjpeg-turbo-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apk add npm nodejs

COPY --from=base /app/yt_dashboard/static/yt_dashboard /app/yt_dashboard/static/yt_dashboard
COPY requirements.txt /app/
RUN pip install --no-cache-dir  -r requirements.txt
# this doesnt change anything
# RUN apk del build-base linux-headers pcre-dev openssl-dev
WORKDIR /app/

COPY . /app

# dit is niet meer nodig of wel?
# COPY yt_dashboard/package.json /app/






RUN cd yt_dashboard && npm install && npm run build



# RUN rm -rf /static
# RUN rm -rf yt_dashboard/node_modules

EXPOSE 80
