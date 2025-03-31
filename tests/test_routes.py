import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_create_term_by_sku():
    sku = "KDWMVZSTP4QSAE5G"
    term_data = {
        "termType": "Reserved",
        "leaseContractLength": "10yr",
        "purchaseOption": "All Upfront",
    }
    response = requests.post(f"{BASE_URL}/skus/{sku}/terms/", json=term_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["termType"] == "Reserved"
    assert response_json["leaseContractLength"] == "10yr"
    assert response_json["purchaseOption"] == "All Upfront"

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_get_pricing_data_with_terms():
    sku = "KDWMVZSTP4QSAE5G"
    term_data = {
        "termType": "OnDemand",
        "leaseContractLength": "1yr",
        "purchaseOption": "All Upfront"
    }
    response_post = requests.post(f"{BASE_URL}/skus/{sku}/terms/", json=term_data)
    assert response_post.status_code == 200

    response_get = requests.get(f"{BASE_URL}/pricing_data/")
    assert response_get.status_code == 200
    data = response_get.json()

    # Guardar la respuesta en un archivo JSON
    with open("pricing_data_response.json", "w") as f:
        json.dump(data, f, indent=4)

    found_sku = False
    found_term = False
    for item in data:
        if item["sku"] == sku:
            found_sku = True
            # Verificamos directamente en item
            if item["termType"] == "OnDemand" and item.get("termAttributes") is None:
                found_term = True
                break

    assert found_sku
    assert found_term

def test_update_term_by_sku():
    sku = "KDWMVZSTP4QSAE5G"
    # Primero, creamos un término para actualizarlo.
    term_data = {
        "termType": "OnDemand",
        "leaseContractLength": "1yr",
        "purchaseOption": "All Upfront",
    }
    create_response = requests.post(f"{BASE_URL}/skus/{sku}/terms/", json=term_data)
    assert create_response.status_code == 200
    created_term = create_response.json()
    #Tomamos el id del termino que se acaba de crear, para usarlo en el update.
    term_type = created_term['termType']

    updated_term_data = {
        "termType": "Reserved",
        "leaseContractLength": "2yr",
        "purchaseOption": "Partial Upfront",
    }
    response = requests.put(f"{BASE_URL}/skus/{sku}/terms/{term_type}", json=updated_term_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["termType"] == "Reserved"
    assert response_json["leaseContractLength"] == "2yr"
    assert response_json["purchaseOption"] == "Partial Upfront"

# def test_delete_term_by_sku():
#     sku = "test-sku-123"
#     term_type = "Reserved"
#     lease_contract_length = "1yr"
#     purchase_option = "No Upfront"

#     # 1️⃣ Verificar que el término existe antes de eliminarlo
#     response_get_before = requests.get(f"{BASE_URL}/pricing_data/")
#     assert response_get_before.status_code == 200
#     data_before = response_get_before.json()
    
#     print("Antes de eliminar:")
#     print(json.dumps(data_before, indent=4))

#     found_term = False
#     for item in data_before:
#         if item["sku"] == sku and item["termType"] == term_type and \
#            item.get("termAttributes") and \
#            item["termAttributes"]["LeaseContractLength"] == lease_contract_length and \
#            item["termAttributes"]["PurchaseOption"] == purchase_option:
#             found_term = True
#             break

#     assert found_term, "El término no se encontró antes de eliminar, no tiene sentido continuar."

#     # 2️⃣ Hacer la solicitud DELETE
#     response_delete = requests.delete(f"{BASE_URL}/skus/{sku}/terms/{term_type}")
#     assert response_delete.status_code == 200, f"Fallo en DELETE: {response_delete.text}"

#     # 3️⃣ Verificar que el término ya no existe después del DELETE
#     response_get_after = requests.get(f"{BASE_URL}/pricing_data/")
#     assert response_get_after.status_code == 200
#     data_after = response_get_after.json()
    
#     print("Después de eliminar:")
#     print(json.dumps(data_after, indent=4))

#     found_term_after = False
#     for item in data_after:
#         if item["sku"] == sku and item["termType"] == term_type and \
#            item.get("termAttributes") and \
#            item["termAttributes"]["LeaseContractLength"] == lease_contract_length and \
#            item["termAttributes"]["PurchaseOption"] == purchase_option:
#             found_term_after = True
#             break

#     assert not found_term_after, "Error: el término con termType 'Reserved' sigue existiendo en la BD después de eliminarlo"

if __name__ == "__main__":
    test_create_term_by_sku()
    test_get_pricing_data_with_terms()
    test_update_term_by_sku()
    # test_delete_term_by_sku()