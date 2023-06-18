# Use an Alpine Linux base image
FROM python:3.10-alpine

# Set the working directory inside the container
WORKDIR /app

# # Copy the necessary files
COPY . .

# Copy requirements.txt
COPY requirements.txt .

# # Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Create a non-root user
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Copy the configuration file
COPY config.py .

# Add command for setup
RUN python - c "from flask_app.model import db,User,BookModel,BookCategory ; config import app ; app.app_context().push() ; db.Create_all()"

# # Set environment variables
ENV FLASK_APP = manager.py
ENV FLASK_RUN_HOST = 0.0.0.0
ENV FLASK_RUN_PORT = 5000

# # Expose the ports on which the Flask app will run
EXPOSE 5000

# # Run the Flask application
CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]