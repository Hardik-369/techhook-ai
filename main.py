import os
import sys
import time

# Add backend to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

import monitor
import transcript
import generator
import image_gen
import poster
import json
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "backend", "data", "logs.json")

def log_event(message, status="success"):
    timestamp = datetime.now().strftime("%I:%M %p")
    log_entry = {"time": timestamp, "msg": message, "status": status}
    
    logs = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r") as f:
                logs = json.load(f)
        except:
            logs = []
            
    logs.insert(0, log_entry) # Add to top
    logs = logs[:20] # Keep last 20 logs
    
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=4)
    print(f"[{timestamp}] {message}")

def run_pipeline():
    log_event("Checking RSS Feed...")
    # 1. Check for new video
    video = monitor.get_latest_video()
    if not video:
        log_event("No videos found in feed.", "error")
        return
        
    if monitor.is_video_processed(video['id']):
        log_event(f"Video {video['id']} already processed.")
        return
        
    log_event(f"New video detected: {video['title']}")
    
    # 2. Get transcript
    log_event("Extracting transcript...")
    ts = transcript.get_transcript(video['id'])
    if not ts:
        log_event("Could not fetch transcript. Skipping.", "error")
        return
        
    # 3. Generate LinkedIn Content
    log_event("Generating AI content with Gemini...")
    content = generator.generate_linkedin_content(ts)
    if not content:
        log_event("AI generation failed.", "error")
        return
        
    # 4. Generate Image
    log_event("Generating hook image with Pillow...")
    image_path = os.path.join("backend", "data", f"{video['id']}.png")
    image_gen.create_hook_image(content['image_hook'], image_path)
    
    # 5. Post to LinkedIn
    log_event("Posting to LinkedIn via Playwright...")
    success = poster.post_to_linkedin(content['post_content'], image_path)
    
    if success:
        log_event("Successfully posted to LinkedIn!")
        monitor.mark_video_processed(video['id'])
    else:
        log_event("Posting failed.", "error")

if __name__ == "__main__":
    run_pipeline()
