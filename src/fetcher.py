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
        os.makedirs(self.data_dir, exist_ok=True)  # Creates the directory if it doesn't exist

    def fetching_data(self):
        """Downloads and saves pricing data to a JSON file."""
        try:
            logger.info(f"Downloading pricing data from: {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()  # Raises an exception for HTTP error codes

            data = response.json()
            file_path = os.path.join(self.data_dir, "pricing_data.json")

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

            logger.info(f"Pricing data saved to: {file_path}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading pricing data: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {e}")
        except OSError as e:
            logger.error(f"Error writing JSON file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
