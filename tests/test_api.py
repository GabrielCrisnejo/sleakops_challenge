import pytest
from fastapi.testclient import TestClient
from src.logger import setup_logger

class TestPricingAPI:
    def test_create_term_by_sku(self, test_client):
        sku = "KDWMVZSTP4QSAE5G"
        term_data = {
            "termType": "Reserved",
            "leaseContractLength": "10yr",
            "purchaseOption": "All Upfront",
        }
        response = test_client.post(f"/skus/{sku}/terms/", json=term_data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["termType"] == "Reserved"
        assert response_json["leaseContractLength"] == "10yr"
        assert response_json["purchaseOption"] == "All Upfront"

    def test_get_pricing_data_with_terms(self, test_client):
        sku = "KDWMVZSTP4QSAE5G"
        term_data = {
            "termType": "OnDemand",
            "leaseContractLength": "1yr",
            "purchaseOption": "All Upfront"
        }
        response_post = test_client.post(f"/skus/{sku}/terms/", json=term_data)
        assert response_post.status_code == 200

        response_get = test_client.get("/pricing_data/")
        assert response_get.status_code == 200
        data = response_get.json()

        found_sku = False
        found_term = False
        for item in data:
            if item["sku"] == sku:
                found_sku = True
                if item["termType"] == "OnDemand":
                    found_term = True
                    break

        assert found_sku
        assert found_term

    def test_update_term_by_sku(self, test_client):
        sku = "KDWMVZSTP4QSAE5G"
        term_data = {
            "termType": "OnDemand",
            "leaseContractLength": "1yr",
            "purchaseOption": "All Upfront",
        }
        create_response = test_client.post(f"/skus/{sku}/terms/", json=term_data)
        assert create_response.status_code == 200
        created_term = create_response.json()
        term_type = created_term['termType']

        updated_term_data = {
            "termType": "Reserved",
            "leaseContractLength": "2yr",
            "purchaseOption": "Partial Upfront",
        }
        response = test_client.put(f"/skus/{sku}/terms/{term_type}", json=updated_term_data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["termType"] == "Reserved"
        assert response_json["leaseContractLength"] == "2yr"
        assert response_json["purchaseOption"] == "Partial Upfront"