FROM node:latest
LABEL authors="Wolkenfarmer, Joshua Riewesell"
WORKDIR /app
RUN npm install -g vite
COPY package*.json ./
RUN npm install
COPY . .
ENV PORT=5173
EXPOSE 5173
CMD ["npm", "run", "dev"]