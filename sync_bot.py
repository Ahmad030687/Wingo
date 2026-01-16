import requests
import time
import firebase_admin
from firebase_admin import credentials, db

# Firebase Setup
cred_dict = {
  "apiKey": "AIzaSyA8qJ3qJl5fzbOBKopx99zsACkEGofbfyY",
  "authDomain": "admin-91a73.firebaseapp.com",
  "databaseURL": "https://admin-91a73-default-rtdb.firebaseio.com",
  "projectId": "admin-91a73",
  "storageBucket": "admin-91a73.firebasestorage.app"
}

# Note: For GitHub Actions, we usually use a service account JSON.
# But for now, we will use a simple requests-based Firebase update if you don't have the JSON.

def fetch_and_save():
    api_url = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageSize=20"
    firebase_url = "https://admin-91a73-default-rtdb.firebaseio.com/wingo_history.json"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        new_items = data['data']['list']
        
        for item in new_items:
            # Check if exists and save to Firebase
            draw_id = item['issueNumber']
            requests.put(f"https://admin-91a73-default-rtdb.firebaseio.com/wingo_history/{draw_id}.json", json=item)
        print("Successfully synced to Firebase!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_save()
