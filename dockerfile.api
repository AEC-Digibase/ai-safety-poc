FROM python:3.11-slim-bullseye

RUN apt-get update
RUN apt-get -y install curl

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project so evals/scripts are available in the container
COPY . .

# If you use an entrypoint script, keep this
RUN chmod +x api/run.sh api/entrypoint.sh

EXPOSE 8000

CMD ["bash", "api/entrypoint.sh"]
# or, if you don't use entrypoint.sh:
# CMD ["bash", "api/run.sh"]
