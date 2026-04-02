FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --loglevel verbose --legacy-peer-deps


COPY . .

EXPOSE 5000

CMD ["npm", "start"]