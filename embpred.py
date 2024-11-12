import requests
import json

# Define the endpoint URL
ENDPOINT_URL = ""

# Define the payload data and give model name from d3x emb list
payload = {
  "model": "",
  "input": "Explain Quanturm computation.",
  "user": "oc"
}

# Define headers
# header is required in sending request from outsize of dkubex environemnt.
headers = {
    "Content-Type": "application/json",
    "Authorization": ""
}
response = requests.post(f"{ENDPOINT_URL}embeddings",json=payload,headers=headers,verify=False)

print("Status Code:", response.status_code)
print("Response Content:", response.text)

# Try to parse the response as JSON if the status code is 200
if response.status_code == 200:
    try:
        print(response.json())
    except json.JSONDecodeError:
        print("Response is not in JSON format.")
else:
    print("Request failed.")
