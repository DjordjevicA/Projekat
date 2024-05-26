# Koristi zvaničnu Python sliku kao osnovu
FROM python:3.9-slim

# Postavi promenljive okruženja
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Postavi radni direktorijum u kontejneru
WORKDIR /app

# Kopiraj datoteku zavisnosti u radni direktorijum
COPY requirements.txt .

# Instaliraj Python zavisnosti
RUN pip install -r requirements.txt

# Kopiraj izvorni kod u radni direktorijum
COPY src/ .


CMD ["openalchemy generate meteoapi.yaml models.py"]
# Otvaranje Flask porta
# EXPOSE 5000

# Komanda za pokretanje Flask aplikacije
# ENTRYPOINT [ "python", "app.py"]
