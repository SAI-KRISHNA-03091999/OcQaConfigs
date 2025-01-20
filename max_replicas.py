import httpx
from openai import OpenAI
from datetime import datetime
import threading
import concurrent.futures
import time

apikey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoic2FuZGVlcC12YW5nYWxhcHVkaSIsInR5cGUiOiJhcGkiLCJpZCI6Ii9kZXBsb3ltZW50L2xsYW1hbmltczIxLyJ9.jT6rmhA7E-iTVq7ZMrfH4ZI9JDECE0ChNkBHcN51zyw"
url = "https://aaf8d7f4e04f44d9cae498875aae23e2-96b785381ba7f842.elb.us-east-2.amazonaws.com/skypilot/d3x/sky-serve-controller-1ca862e8-1ca8/30003/v1/"
model = "meta/llama3-8b-instruct"

# Define the messages for the chat model
messages = [
    {"role": "user", "content": "Hello! How are you?"},
    {"role": "assistant", "content": "Hi! I am quite well, how can I help you today?"},
    {"role": "user", "content": "Who is Arjuna?"}
]

def send_request(client: OpenAI, request_id: int):
    """
    Sends a single request to the chat model and logs the response.
    """
    try:
        start_time = datetime.now()
        thread_name = threading.current_thread().name
        print(f"Request {request_id} started at {start_time} in thread {thread_name}")

        chat_response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=32,
            stream=False
        )
        assistant_message = chat_response.choices[0].message

        end_time = datetime.now()
        print(f"Request {request_id} completed at {end_time} in thread {thread_name} - Assistant: {assistant_message}")
    except Exception as e:
        print(f"Request {request_id} failed with error: {e}")

def main():
    """
    Sends 200 parallel requests per second using ThreadPoolExecutor.
    """
    httpx_client = httpx.Client(verify=False)  # Synchronous HTTP client
    client = OpenAI(base_url=url, api_key=apikey, http_client=httpx_client)

    request_id = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        while True:
            tasks = []
            print("\nSending batch of 200 requests...")
            for _ in range(100):  # Sending 200 requests per batch
                request_id += 1
                tasks.append(executor.submit(send_request, client, request_id))

            # Wait for all tasks to complete
            concurrent.futures.wait(tasks)

            # Sleep for 1 second to maintain the requests per second rate
            print("Batch completed. Waiting for the next second...")
            time.sleep(1)

    httpx_client.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nLoad test stopped by user.")
