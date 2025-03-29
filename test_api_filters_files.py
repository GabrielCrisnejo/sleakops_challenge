import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000/pricing_data/"
OUTPUT_DIR = "api_responses"  # Directorio para guardar los archivos JSON

# Crear el directorio si no existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_filename(filters):
    """Genera un nombre de archivo basado en los filtros."""
    parts = []
    for key, value in filters.items():
        parts.append(f"{key}-{value}")
    return "_".join(parts) + ".json" if parts else "all_data.json"

def test_api_filters(filters):
    """Prueba la API con los filtros y guarda la respuesta en un archivo JSON."""
    try:
        response = requests.get(BASE_URL, params=filters)
        response.raise_for_status()
        data = response.json()

        filename = os.path.join(OUTPUT_DIR, generate_filename(filters))
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Respuesta guardada en: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error con filtros {filters}: {e}")

if __name__ == "__main__":
    filters_list = [
        # {"databaseEngine": "MySQL"},
        # {"instanceType": "db.r5.large"},
        # {"vcpu": 4},
        # {"memory": "16 GiB"},
        {"databaseEngine": "PostgreSQL", "instanceType": "db.r6g.large"},
        # {"databaseEngine": "SQL Server", "vcpu": 8, "memory": "32 GiB"},
        # {"instanceType": "db.m5.xlarge", "memory": "16 GiB"},
        # {"databaseEngine": "MySQL", "instanceType": "db.r5.large", "vcpu": 4, "memory": "16 GiB"},
        # {}  # Sin filtros (todos los datos)
    ]

    for filters in filters_list:
        test_api_filters(filters)