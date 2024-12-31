import requests
import time
import json

bot_token = "7227008474:AAHfFTIOxU8MX6LDDQd7C5K-MXD0PImNJz0"
from_chat_id = "-1001800348098"
to_chat_id = "-1001972766787"
admin_chat_id = "6573541531"  # Admin chat ID, replace with actual ID

# Function to send copyMessages request with a batch of message IDs
def send_copy_messages_request(from_chat_id, to_chat_id, message_ids):
    url = f"https://api.telegram.org/bot{bot_token}/copyMessages?chat_id={to_chat_id}&from_chat_id={from_chat_id}&message_ids={json.dumps(message_ids)}"
    response = requests.get(url)
    return response.json()

# Function to send a message to the admin chat
def send_admin_message(text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": admin_chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)
    return response.json()

# Batch size kitni ID ek request mein bhejni hai
batch_size = 100  # Adjust this value as needed

# Loop through message IDs from 100000 to 150000 in batches
for start_id in range(4321, 294280, batch_size):
    end_id = min(start_id + batch_size - 1, 150000)
    message_ids = list(range(start_id, end_id + 1))

    result = send_copy_messages_request(from_chat_id, to_chat_id, message_ids)
    
    if not result['ok'] and result['error_code'] == 429:
        wait_time = result['parameters']['retry_after']
        print(f"Too Many Requests. Waiting for {wait_time} seconds...")
        time.sleep(wait_time)
        # Retry the same batch after waiting
        result = send_copy_messages_request(from_chat_id, to_chat_id, message_ids)
    
    log_message = f"Message IDs {start_id} to {end_id}: {result}"
    print(log_message)

    # Send log to admin chat
    send_admin_message(log_message)

    # Extra sleep to avoid hitting the rate limit frequently
    time.sleep(2)
