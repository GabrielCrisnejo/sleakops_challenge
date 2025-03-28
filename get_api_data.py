import requests
import json
import os

def get_pricing_data(base_url, params=None, output_file="pricing_data.json"):
    """Realiza una solicitud GET a la API y guarda la respuesta JSON en un archivo."""
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP (4xx o 5xx)
        data = response.json()

        # Guarda los datos JSON en un archivo
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)  # Indentación para mejor legibilidad

        print(f"Respuesta de la API guardada en: {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud a la API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
    except OSError as e:
        print(f"Error al escribir el archivo JSON: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    base_url = "http://127.0.0.1:8000/pricing_data/"
    filters = {"databaseEngine": "MySQL"}  # Ejemplo de filtro
    output_file = "pricing_data_mysql.json"  # Nombre del archivo de salida

    get_pricing_data(base_url, params=filters, output_file=output_file)