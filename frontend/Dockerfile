FROM node:latest
LABEL authors="Wolkenfarmer, Joshua Riewesell"
WORKDIR /app
RUN npm install -g vite
RUN if [ "$RUN_CONFIG" = "prod" ]; then npm install -g serve; fi
COPY package*.json ./
RUN npm install
COPY . .
ARG RUN_CONFIG
ARG SERVER_URL
ENV VITE_SERVER_URL=$SERVER_URL
ENV PORT=5173
EXPOSE 5173
RUN if [ "$RUN_CONFIG" = "prod" ]; then npm run build-only; fi
CMD if [ "$RUN_CONFIG" = "prod" ]; then serve -s dist -l 5173; else npm run dev; fi