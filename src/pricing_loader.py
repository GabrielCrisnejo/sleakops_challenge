import requests
import json
import logging
import os
from src.config import PRICING_URL, DATA

# Configuración de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PricingDataLoader:
    def __init__(self, url, data_dir):
        self.url = url
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True) # Crea el directorio si no existe

    def load_pricing_data(self):
        """Descarga y guarda los datos de precios en un archivo JSON."""
        try:
            logger.info(f"Descargando datos de precios desde: {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP

            data = response.json()
            file_path = os.path.join(self.data_dir, "pricing_data.json")

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

            logger.info(f"Datos de precios guardados en: {file_path}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error al descargar datos de precios: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar la respuesta JSON: {e}")
        except OSError as e:
            logger.error(f"Error al escribir el archivo JSON: {e}")
        except Exception as e:
            logger.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    loader = PricingDataLoader(PRICING_URL, DATA)
    loader.load_pricing_data()