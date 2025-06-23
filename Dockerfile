# Use a minimal Python image
FROM python:3.11-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Expose the dynamic port (App Runner will assign this)
EXPOSE 8501

# Run using shell so $PORT is interpreted correctly
CMD ["sh", "-c", "streamlit run car_dashboard.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false"]
