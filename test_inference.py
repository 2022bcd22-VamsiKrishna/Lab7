import requests
import sys

API_URL = "http://host.docker.internal:8000/predict" 

valid_payload = {
    "features": [7.4, 0.7, 0.0, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4]
}

invalid_payload = {
    "features": ["invalid_string", 0.7, 0.0, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4]
}

def test_valid_request():
    print("--- Stage 4: Testing Valid Request ---")
    response = requests.post(API_URL, json=valid_payload)
    
    if response.status_code != 200:
        print(f"Failed: Expected status 200, got {response.status_code} - {response.text}")
        sys.exit(1)
        
    data = response.json()
    
    if "wine_quality" not in data: 
        print("Failed: 'wine_quality' field missing")
        sys.exit(1)
        
    if not isinstance(data["wine_quality"], (int, float, list)):
        print("Failed: Prediction is not numeric")
        sys.exit(1)
        
    print(f"Success! Prediction received: {data['wine_quality']}")

def test_invalid_request():
    print("--- Stage 5: Testing Invalid Request ---")
    response = requests.post(API_URL, json=invalid_payload)
    
    if response.status_code == 200:
        print("Failed: API should have returned an error for invalid input")
        sys.exit(1)
        
    print(f"Success! API correctly handled invalid input. Error: {response.status_code}")

if __name__ == "__main__":
    try:
        test_valid_request()
        test_invalid_request()
    except Exception as e:
        print(f"Exception occurred: {e}")
        sys.exit(1)