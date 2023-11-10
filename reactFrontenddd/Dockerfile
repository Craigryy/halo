# Use the official Node.js image as the base image
FROM node:14.17.6 AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies and clean up unnecessary files
RUN npm install

# Copy the rest of the frontend files
COPY . .

# Build the React app
RUN npm run build

# Expose the port on which the React app will run
EXPOSE 3000

# Create a startup script to run the React app
CMD ["npm", "start"]
