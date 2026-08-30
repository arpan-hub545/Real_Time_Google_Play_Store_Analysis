# Use an official Python runtime as a parent image
FROM python:3.11.5-slim-bullseye

# Set the working directory in the container
WORKDIR /code

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Update OS packages and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#Production: Collect static files (optional, but necessary if Nginx doesn't handle static files)
EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
#use