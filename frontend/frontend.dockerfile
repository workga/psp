# CURRENTLY DOESN'T WORK!
FROM node:20

ENV CHOKIDAR_USEPOLLING=true

COPY frontend/package.json frontend/package-lock.json ./

RUN npm install

COPY makefile ./

EXPOSE 8090
ENTRYPOINT ["make", "frontend"]