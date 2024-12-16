FROM node:22.9.0

WORKDIR /app

RUN apt-get update && apt-get install -y \
  libcairo2-dev \
  libpango1.0-dev \
  libjpeg-dev \
  libgif-dev \
  librsvg2-dev

COPY package*.json ./

ENV npm_config_build_from_source=true

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]