FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50053

RUN apt-get update && apt-get install -y supervisor \
    wget unzip fonts-liberation libglib2.0-0 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgtk-3-0 libasound2 \
    && apt-get install -y firefox-esr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/lib/firefox-esr/distribution \
    && echo '{ "policies": { "DisableTelemetry": true, "DisableFirefoxStudies": true, "DisableAppUpdate": true, "DisableDefaultBrowserAgent": true } }' > /usr/lib/firefox-esr/distribution/policies.json

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# CMD ["python", "sugma_balls.py"]