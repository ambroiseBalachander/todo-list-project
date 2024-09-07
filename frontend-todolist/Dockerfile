# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy your static files and index.html to the appropriate directory in the Nginx container
COPY . /usr/share/nginx/html

# Copy the custom Nginx configuration file to the container
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
