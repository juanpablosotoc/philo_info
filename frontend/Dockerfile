FROM node:18-alpine

WORKDIR /app

COPY . .

RUN npm install --production

EXPOSE 3000

RUN npm i --save-dev @types/react-helmet

CMD ["npm", "start"]
