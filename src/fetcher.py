import requests
import json
import os
from src.settings import PRICING_URL, DATA
from src.logger import setup_logger

# Logger configuration
logger = setup_logger("fetcher")

class FetcherData:
    def __init__(self, url, data_dir):
        self.url = url
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True) # Crea el directorio si no existe

    def fetching_data(self):
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
    loader = FetcherData(PRICING_URL, DATA)
    loader.fetching_data()