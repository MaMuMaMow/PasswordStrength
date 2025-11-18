import requests
import json

#_______________________________input__________________________________________
try:
    url = "http://(your url)/checkStrength" #change URL here. for exmple : http://127.0.0.1:8000/checkStrength
    password = input("Enter your password : ")
    payload = {"password": password,
               "request_id": "test123"  #optional
               }
    response = requests.post(url, json=payload) #the API have input and output as JSON. So you have to request as JSON
    response.raise_for_status()
    data = response.json()
#_______________________________output__________________________________________
        
    print(f"Status Code: {response.status_code}")

    for item in data.get("data", []):
        if item["id"] == 0:
            print(item["reason"])
        else:
            print(item["reason"])
        

    if "metadata" in data:
        print("\nMetadata:")
        print(f"Time: {data['metadata']['time']}")
        print(f"API Version: {data['metadata']['API version']}")

#_______________________________in case that there's an error__________________________________________

except requests.exceptions.ConnectionError:
    print("! Error: Could not connect to the API server.")
    print("   Make sure the API server is running (using uvicorn).")

except requests.exceptions.RequestException as e:
    print(f"! Error making request: {e}")

except json.JSONDecodeError as e:
    print(f"! Error parsing API response: {e}")
     
except Exception as e:
    print(f"! Unexpected error: {e}")

