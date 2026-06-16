# Use the official Node.js 24 slim image
FROM node:24-slim

# Set the working directory
WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package.json and pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["pnpm", "exec", "tsx", "index.ts"]
