# Use a lightweight Python image
FROM python:3.11-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8501

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Expose the expected port
EXPOSE $PORT

# Run your Streamlit app on the correct port & address
CMD streamlit run car_dashboard.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=false
