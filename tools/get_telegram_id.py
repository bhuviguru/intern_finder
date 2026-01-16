import requests
import time
import os
from dotenv import load_dotenv

def get_chat_id():
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token or token == "your_bot_token":
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        return

    print(f"🔑 Using Token: {token[:5]}...{token[-5:]}")
    
    # 1. Verify Bot Identity
    url_me = f"https://api.telegram.org/bot{token}/getMe"
    try:
        resp = requests.get(url_me)
        data = resp.json()
        if not data.get('ok'):
            print(f"❌ Invalid Token! Telegram says: {data.get('description')}")
            return
        
        bot_user = data['result']['username']
        bot_name = data['result']['first_name']
        print(f"✅ Token works! Bot Name: '{bot_name}' | Username: @{bot_user}")
        print(f"👉 Please go to https://t.me/{bot_user} and send 'Hello'")
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    # 2. Get Updates
    print("⏳ Listening for messages...")
    url_updates = f"https://api.telegram.org/bot{token}/getUpdates"
    
    # Clear old updates first? No, we want to see if the 'hlo' is there.
    
    start_time = time.time()
    while time.time() - start_time < 60: # Run for 60 seconds
        try:
            response = requests.get(url_updates)
            data = response.json()
            
            if data.get('result'):
                for update in data['result']:
                    if 'message' in update:
                        chat = update['message']['chat']
                        print("\n✅ MESSAGE RECEIVED!")
                        print(f"📩 Text: {update['message'].get('text')}")
                        print(f"🆔 CHAT ID: {chat['id']}")
                        print(f"👤 Name: {chat.get('first_name')} (@{chat.get('username')})")
                        return # Exit on success
            
            time.sleep(2)
            print(".", end="", flush=True)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

    print("\n❌ No message received in 60 seconds. Try sending another message!")

if __name__ == "__main__":
    get_chat_id()
