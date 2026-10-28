# Vybereme oficiální Python image (např. verze 3.11)
FROM python:3.11-slim

# Nastavíme pracovní adresář v kontejneru
WORKDIR /app

# Django settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Zkopírujeme soubor requirements.txt do kontejneru
COPY requirements.txt .

# Nainstalujeme python závislosti
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --retries 5 --default-timeout=100 -r requirements.txt

# Zkopírujeme celý projekt do kontejneru
COPY . .

# Otevřeme port (ten, na kterém běží Django)
EXPOSE 60000

# Make entry file executable
RUN chmod +x /app/entrypoint.prod.sh

# Nastavíme proměnné prostředí, aby Django používalo správné nastavení
ENV DJANGO_SETTINGS_MODULE=backend.production

# Spustíme Django server pomocí Gunicorn (produkční server)
CMD ["/app/entrypoint.prod.sh"]
