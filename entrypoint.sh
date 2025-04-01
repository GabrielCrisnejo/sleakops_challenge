#!/bin/sh

# # Esperar a que la base de datos esté lista
# until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -W -c '\q'; do
#   echo "Waiting for database to be ready..."
#   sleep 2
# done

# echo "Database is ready!"

# Ejecutar las migraciones de Alembic
alembic upgrade head

# Ejecutar main.py para cargar los datos
python main.py

# Iniciar la API
uvicorn main:app --host 0.0.0.0 --port 8000