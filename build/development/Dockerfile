FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

# gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN apk update
RUN apk add gcc xvfb musl-dev libffi-dev openssl-dev postgresql-dev zlib-dev jpeg-dev bash openssl-dev wkhtmltopdf curl build-base
RUN apk add npm nodejs

COPY . /app
ADD requirements.txt /app/
COPY yt_dashboard/package.json /app/
WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# RUN python setup.py build
# RUN python setup.py install

# ARG DATABASE_URL
# RUN python manage.py migrate

#EXPOSE 80
