
import requests
import time
import sys

def test_api():
    base_url = "http://127.0.0.1:5000/api"
    
    print("Waiting for server...")
    time.sleep(15) 

    try:
        # Test 1: Metrics
        print("Testing /metrics...")
        resp = requests.get(f"{base_url}/metrics")
        print(f"Status: {resp.status_code}")
        print(resp.json())

        # Test 2: History
        print("\nTesting /history...")
        resp = requests.get(f"{base_url}/history?hours=5")
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Returned {len(data.get('values', []))} historical points.")

        # Test 3: Predict Hour (Single)
        print("\nTesting /predict_hour (Single)...")
        resp = requests.get(f"{base_url}/predict_hour?model=single")
        print(f"Status: {resp.status_code}")
        print(resp.json())

        # Test 4: Predict 24h
        print("\nTesting /predict_24h...")
        resp = requests.get(f"{base_url}/predict_24h?model=single")
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Forecast points: {len(data.get('forecast', []))}")

    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_api()
