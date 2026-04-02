FROM node:18

WORKDIR / 

COPY package.json package-lock.json ./

RUN npm install --loglevel verbose --legacy-peer-deps


COPY . .

ENV HOST=0.0.0.0
ENV BROWSER=none

EXPOSE 3000

CMD ["npm", "start"]