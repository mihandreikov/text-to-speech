# Use the official Nginx image as the base image
FROM nginx:alpine

# Copy your HTML files into the Nginx document root
COPY . /usr/share/nginx/html

# Expose port 80, which is the default HTTP port for Nginx
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]