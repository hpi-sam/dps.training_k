FROM node:latest
LABEL authors="Wolkenfarmer, Joshua Riewesell"
WORKDIR /app
# set env vars to persist them in the image
ARG VITE_RUN_CONFIG
ARG VITE_SERVER_URL_HTTP
ARG VITE_SERVER_URL_WS
RUN npm install -g vite
RUN if [ "$VITE_RUN_CONFIG" = "prod" ]; then npm install -g serve; fi
COPY package*.json ./
RUN npm install
COPY . .
ENV VITE_RUN_CONFIG=${VITE_RUN_CONFIG}
ENV VITE_SERVER_URL_HTTP=${VITE_SERVER_URL_HTTP}
ENV VITE_SERVER_URL_WS=${VITE_SERVER_URL_WS}
ENV PORT=5173
EXPOSE 5173
RUN if [ "$VITE_RUN_CONFIG" = "prod" ]; then npm run build-only; fi
CMD if [ "$VITE_RUN_CONFIG" = "prod" ]; then serve -s dist -l 5173; else npm run dev; fi