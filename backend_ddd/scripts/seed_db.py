import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"
api_url = BASE_URL + "/create-closed-loop"
data = {
    "name": "LUMS",
    "logo_url": "www.no-logo.com",
    "description": "Best university omg???",
    "verification_type": "ROLLNUMBER",
    "regex": "2[\d]{7}",
}

response = requests.post(api_url, json=data)

if response.status_code == 201:
    print("Closed loop created successfully!")
else:
    print("Error creating Closed loop:", response.status_code)
    print(response.json())
