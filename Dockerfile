# Dockerfile

# 1. Use an official Python runtime as a parent image
# Using a slim image reduces the final image size
FROM python:3.11-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file into the container
# Copy only requirements first to leverage Docker cache
COPY requirements.txt ./

# 4. Install any needed packages specified in requirements.txt
# --no-cache-dir reduces image size further
# --upgrade pip ensures we have the latest pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code into the container
COPY . .

# 6. Make port 8080 available to the world outside this container
# This informs Docker that the container listens on this port
EXPOSE 8080

# 7. Define the command to run the application using Gunicorn
# Binds Gunicorn to listen on all interfaces (0.0.0.0) on port 8080
# --- MODIFIED LINE BELOW ---
# Assumes your Flask app object is named 'app' in the file named 'main.py'
# Adjust 'main:app' if your Flask object name is different (e.g., 'main:my_flask_app')
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]