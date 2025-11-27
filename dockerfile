FROM python:3.11-slim

WORKDIR /app

# Install deps first (layer cache-friendly)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (api, evals, scripts, etc.)
COPY . .

# Just in case, ensure entrypoint is executable
RUN chmod +x api/run.sh api/entrypoint.sh

EXPOSE 8000

# Use the entrypoint that does pre-flight and then starts the API
CMD ["bash", "api/entrypoint.sh"]
