# FROM python:3.12.2

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# RUN apt-get update && apt-get install -y postgresql-client

# COPY . .

# COPY alembic.ini ./alembic.ini

# # Asegurar permisos de lectura para los scripts de migración
# RUN chmod -R +r alembic

# CMD ["./entrypoint.sh"]

FROM python:3.12.2

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

COPY . .

COPY alembic.ini ./alembic.ini

# Asegurar permisos de lectura para los scripts de migración
RUN chmod -R +r alembic

CMD ["python", "main.py"]