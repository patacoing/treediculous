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
RUN npm run build

FROM nginx:alpine
COPY --from=build /build/dist/ /usr/share/nginx/html