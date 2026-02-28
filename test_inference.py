import requests
import sys
import time

API_URL = "http://host.docker.internal:8000/predict"

valid_payload = {
    "fixed_acidity": 7.4, "volatile_acidity": 0.7, "citric_acid": 0.0, 
    "residual_sugar": 1.9, "chlorides": 0.076, "free_sulfur_dioxide": 11.0, 
    "total_sulfur_dioxide": 34.0, "density": 0.9978, "pH": 3.51, 
    "sulphates": 0.56, "alcohol": 9.4
}

invalid_payload = {
    "fixed_acidity": "invalid_string_instead_of_float", 
    "volatile_acidity": 0.7
}

def test_valid_request():
    print("--- Stage 4: Testing Valid Request ---")
    response = requests.post(API_URL, json=valid_payload)
    
    if response.status_code != 200:
        print(f"Failed: Expected status 200, got {response.status_code}")
        sys.exit(1)
        
    data = response.json()
    if "prediction" not in data: 
        print("Failed: 'prediction' field missing")
        sys.exit(1)
        
    if not isinstance(data["prediction"], (int, float, list)): 
        print("Failed: Prediction is not numeric")
        sys.exit(1)
        
    print(f"Success! Prediction received: {data['prediction']}")

def test_invalid_request():
    print("--- Stage 5: Testing Invalid Request ---")
    response = requests.post(API_URL, json=invalid_payload)
    
    if response.status_code == 200: 
        print("Failed: API should have returned an error for invalid input")
        sys.exit(1)
        
    print(f"Success! API correctly handled invalid input. Error: {response.text}") 

if __name__ == "__main__":
    try:
        test_valid_request()
        test_invalid_request()
    except Exception as e:
        print(f"Exception occurred: {e}")
        sys.exit(1)