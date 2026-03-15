FROM node:latest
LABEL authors="Wolkenfarmer, Joshua Riewesell"
WORKDIR /app

# set env vars to persist them in the image
ARG REACT_APP_RUN_CONFIG=dev
ARG REACT_APP_VUE_URL=http://localhost:5173

# Install global packages
RUN npm install -g serve

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Set environment variables
ENV REACT_APP_RUN_CONFIG=${REACT_APP_RUN_CONFIG}
ENV REACT_APP_VUE_URL=${REACT_APP_VUE_URL}
ENV IS_DOCKER=TRUE
ENV PORT=3000

EXPOSE 3000

# Build for production if needed
RUN if [ "$REACT_APP_RUN_CONFIG" = "prod" ]; then npm run build; fi

# Run based on configuration
CMD if [ "$REACT_APP_RUN_CONFIG" = "prod" ]; then serve -s build -l 3000; else npm run dev; fi
