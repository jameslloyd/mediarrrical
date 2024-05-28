FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./ 

# Set up cron
#RUN apt-get update && apt-get install -y cron
#RUN touch /var/log/cron.log
#RUN chmod 0644 /var/log/cron.log
#RUN crontab -l | { cat; echo "18 * * * * python /app/main.py"; } | crontab -

#CMD ["cron", "-f"]
CMD ["python", "main.py"]