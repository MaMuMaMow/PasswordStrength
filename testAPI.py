import requests
import json
from datetime import datetime

def test_password_strength():
    url = "http://127.0.0.1:8000/checkStrength"
    
    try:
        
        password = input("Enter your password to check strength: ")
        payload = {"password": password}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        print(f"Status Code: {response.status_code}")

        if "data" in data:
            for result in data["data"]:
                if result["id"] == 0:
                    print("✅", result["reason"])
                else:
                    print("❌", result["reason"])
        
        if "metadata" in data:
            print("\nMetadata:")
            print(f"Time: {data['metadata']['time']}")
            print(f"API Version: {data['metadata']['API version']}")
            
    except requests.exceptions.ConnectionError:
        print("\n! Error: Could not connect to the API server.")
        print("   Make sure the API server is running (using uvicorn).")

    except requests.exceptions.RequestException as e:
        print(f"\n! Error making request: {e}")

    except json.JSONDecodeError as e:
        print(f"\n! Error parsing API response: {e}")
        
    except Exception as e:
        print(f"\n! Unexpected error: {e}")

test_password_strength()