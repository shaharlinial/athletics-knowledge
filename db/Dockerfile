# Use the official MySQL image as a parent image
FROM mysql:5.7

# Set the root password and create the database
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=mydatabase

# Copy the initialization script into the container
COPY init.sql /docker-entrypoint-initdb.d/