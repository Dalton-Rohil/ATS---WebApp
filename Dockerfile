# Base Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false"]
