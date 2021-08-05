FROM node:slim
EXPOSE 8080
WORKDIR /app
COPY package.json /app/
RUN npm install
COPY server.js /app/
CMD node /app/server.js