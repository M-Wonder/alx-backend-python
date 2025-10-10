# Use an official Python runtime as the base image
FROM python:3.10

# Set environment variables to prevent Python from buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django project into the container
COPY . /app/

# Expose the port your Django app runs on (default: 8000)
EXPOSE 8000

# Run the Django development server (binding to all network interfaces)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "-p", "8000"]
