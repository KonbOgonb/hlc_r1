FROM python:3.6.2-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY /app /app
COPY /tmp /tmp
COPY ./docker-entrypoint.sh /app

# Install any needed packages specified in requirements.txt
RUN pip install flask
RUN pip install gunicorn
RUN pip install python3-memcached
RUN apt-get update
RUN apt-get install -y memcached

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["sh", "docker-entrypoint.sh"]