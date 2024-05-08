# Use python image
FROM python:3.8.16-slim-bullseye

# install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends graphviz && \
    rm -rf /var/lib/apt/lists/*  && \
    python -m pip install --no-cache-dir --upgrade pip==23.0.* setuptools==58.0.*

# Copy the current directory contents into the container
COPY SemDesLC /app/
COPY requirements.txt /app/
COPY app.py		/app/
# Working directory in the container
WORKDIR /app

# Install any needed dependencies specified in requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]