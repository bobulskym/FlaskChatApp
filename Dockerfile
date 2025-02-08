# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy only necessary files to the container
COPY app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
