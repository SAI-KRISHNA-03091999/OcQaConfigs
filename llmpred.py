from openai import OpenAI
import requests
import httpx
url= ""
apikey = ""

r = requests.get(f"{url}/models",  headers = {"Authorization": f"Bearer {apikey}"}, verify=False)
if r.status_code != 200:
    print(r.text, flush=True)
assert r.status_code == 200, "unable to get the model details"
models = r.json()
model = None
if "data" in models  and len(models["data"]) > 0:
    model = models["data"][0]["id"]
httpx_client = httpx.Client(verify=False)
client = OpenAI(base_url=url, api_key=apikey , http_client= httpx_client)
messages = [
    {"role": "user", "content": "Hello! How are you?"},
    {"role": "assistant", "content": "Hi! I am quite well, how can I help you today?"},
    {"role": "user", "content": "Write a short limerick about the wonders of GPU computing."}
]
chat_response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=32,
    stream=False
)
assistant_message = chat_response.choices[0].message
print(assistant_message)

