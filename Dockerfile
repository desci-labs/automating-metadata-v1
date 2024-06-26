# Use a base image with Python installed
FROM python:3.9

# Set the working directory in the container
WORKDIR /

# we put this before the COPY app step just to cache the installation of the requirements, so if we make code changes without requirements updates builds are faster
COPY ./app/requirements.txt ./app/requirements.txt
RUN pip install -r ./app/requirements.txt

# Copy the script and requirements file into the container
COPY ./app ./app

# Install dependencies
RUN pip install gunicorn

#run service - Expose (what is the request response model)
EXPOSE 5001
EXPOSE 5005

ENV FLASK_APP=server.py

WORKDIR /app

# Define the command to run when the container starts
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
# gunicorn is a production ready web server for flask, with ability to handle multiple requests
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "server:app"]