import requests
import json
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000/pricing_data/"
OUTPUT_DIR = "example/api_responses"  # Directory to store JSON response files

def setup_output_directory():
    """Create the output directory if it doesn't exist."""
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

def generate_filename(filters):
    """Generate a filename based on the applied filters.
    
    Args:
        filters (dict): Dictionary of filter parameters
        
    Returns:
        str: Generated filename with format 'key1-value1_key2-value2.json'
             or 'all_data.json' if no filters applied
    """
    if not filters:
        return "all_data.json"
    return "_".join(f"{key}-{value}" for key, value in filters.items()) + ".json"

def test_api_with_filters(filters):
    """Test the API with given filters and save response to JSON file.
    
    Args:
        filters (dict): Dictionary of filter parameters to test
    """
    try:
        response = requests.get(BASE_URL, params=filters)
        response.raise_for_status()
        data = response.json()

        filename = os.path.join(OUTPUT_DIR, generate_filename(filters))
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Response saved to: {filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error with filters {filters}: {e}")
        return False

def main():
    """Main function to execute API filter tests."""
    setup_output_directory()
    
    test_cases = [
        {"databaseEngine": "MySQL"},
        {"instanceType": "db.r5.large"},
        {"vcpu": 4},
        {"memory": "16 GiB"},
        {"databaseEngine": "PostgreSQL", "instanceType": "db.r6g.large"},
        {"databaseEngine": "SQL Server", "vcpu": 8, "memory": "32 GiB"},
        {"instanceType": "db.m5.xlarge", "memory": "16 GiB"},
        {"databaseEngine": "MySQL", "instanceType": "db.r5.large", "vcpu": 4, "memory": "16 GiB"},
        {}  # No filters (all data)
    ]

    for test_case in test_cases:
        test_api_with_filters(test_case)

if __name__ == "__main__":
    main()