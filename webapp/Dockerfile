FROM node:latest AS build
WORKDIR /build

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm ci

COPY src src
COPY public public
COPY index.html index.html
COPY vite.config.js vite.config.js
COPY postcss.config.js postcss.config.js
COPY tailwind.config.js tailwind.config.js
COPY public/ads.txt ads.txt
RUN npm run build

FROM caddy:latest
COPY --from=build /build/dist/ /srv/
COPY Caddyfile /etc/caddy/Caddyfile