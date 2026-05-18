import os
import requests
from dotenv import load_dotenv

# 1. This line finds your .env file and reads the key
load_dotenv()
API_KEY = os.getenv("CLIMATIQ_API_KEY")

# 2. Setup the API request
url = "https://api.climatiq.io/data/v1/estimate"
headers = {"Authorization": f"Bearer {API_KEY}"}

# We'll ask for the carbon footprint of 1000kg of Steel
# Change your payload to use this verified ID for generic steel
payload = {
    "emission_factor": {
        "activity_id": "metals-type_steel_section", # A more common standard ID
        "data_version": "^0" # This tells it to use the latest version of this factor
    },
    "parameters": {
        "weight": 1000,
        "weight_unit": "kg"
    }
}

print("Connecting to Climatiq API...")
try:
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Carbon for 1000kg Steel: {data['co2e']} {data['co2e_unit']}")
    else:
        print(f"❌ Failed! Error code: {response.status_code}")
        print(f"Message: {response.text}")

except Exception as e:
    print(f"❌ Connection Error: {e}")