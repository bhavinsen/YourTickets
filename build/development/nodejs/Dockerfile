FROM node:lts-alpine

COPY . /app

WORKDIR /app/yt_dashboard
RUN npm install

#COPY build/development/nodejs/start.sh /start.sh
#RUN sed -i 's/\r//' /start.sh
#RUN chmod +x /start.sh

EXPOSE 8080