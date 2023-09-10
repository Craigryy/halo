# Specify the base image
FROM python:3.10-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files
COPY . .

# Upgrade setuptools
RUN pip install --upgrade setuptools

# Install yaml
RUN pip install PyYAML

# Install the Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Set environment variables
ENV POSTGRES_HOST=database
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=halo
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=Favour98
ENV POSTGRES_SECRET_KEY=jesusislord
ENV FLASK_PORT=5000

# Expose the ports on which the Flask app will run and the PostgreSQL server
EXPOSE 5000
EXPOSE 5432

# Set the command to run the Flask app
CMD ["python", "manager.py"]
