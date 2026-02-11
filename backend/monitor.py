import feedparser
import json
import os

FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCvX6nS2IqPlo_X7M8d8iOsw"
STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "store.json")

def get_latest_video():
    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        return None
    
    latest_entry = feed.entries[0]
    return {
        "id": latest_entry.yt_videoid,
        "link": latest_entry.link,
        "title": latest_entry.title,
        "published": latest_entry.published
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
