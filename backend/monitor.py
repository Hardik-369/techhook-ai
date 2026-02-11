import json
import os
import requests
import re

FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCsQoiOrh7jzKmE8NBofhTnQ"
STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "store.json")

def get_video_description(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        r = requests.get(url, timeout=10)
        # Use regex to find the short description in the page source
        match = re.search(r'\"shortDescription\":\"(.*?)\"', r.text)
        if match:
            # Clean up escape characters
            return match.group(1).encode().decode('unicode_escape')
        return ""
    except Exception as e:
        print(f"Error fetching description: {e}")
        return ""

def get_latest_video():
    import feedparser
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        return None
    
    latest_entry = feed.entries[0]
    video_id = latest_entry.yt_videoid
    return {
        "id": video_id,
        "link": latest_entry.link,
        "title": latest_entry.title,
        "published": latest_entry.published,
        "description": get_video_description(video_id)
    }

def is_video_processed(video_id):
    if not os.path.exists(STORE_PATH):
        return False
    
    with open(STORE_PATH, "r") as f:
        data = json.load(f)
        return video_id in data.get("processed_ids", [])

def mark_video_processed(video_id):
    if not os.path.exists(os.path.dirname(STORE_PATH)):
        os.makedirs(os.path.dirname(STORE_PATH))
    
    data = {"processed_ids": []}
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, "r") as f:
            data = json.load(f)
            
    if video_id not in data["processed_ids"]:
        data["processed_ids"].append(video_id)
        
    with open(STORE_PATH, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    latest = get_latest_video()
    if latest:
        print(f"Latest video: {latest['title']} ({latest['id']})")
        if not is_video_processed(latest['id']):
            print("New video detected!")
        else:
            print("Video already processed.")
