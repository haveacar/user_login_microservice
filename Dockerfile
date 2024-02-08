# Stage 1: Build and test stage
FROM python:3.11-slim AS builder

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application's requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest


COPY . .

# Set PYTHONPATH to include the current directory
ENV PYTHONPATH=/usr/src/app

# Run tests
RUN pytest
# Stage 2: Production stage
FROM python:3.11-slim AS production

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the artifacts needed from the builder stage
COPY --from=builder /usr/src/app /usr/src/app

# Install runtime dependencies only
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=application.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run application.py
CMD ["flask", "run"]