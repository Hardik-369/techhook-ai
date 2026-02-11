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

def run_pipeline():
    print("Starting TechHook AI Pipeline...")
    
    # 1. Check for new video
    video = monitor.get_latest_video()
    if not video:
        print("No videos found in feed.")
        return
        
    if monitor.is_video_processed(video['id']):
        print(f"Video {video['id']} already processed.")
        return
        
    print(f"New video detected: {video['title']}")
    
    # 2. Get transcript
    ts = transcript.get_transcript(video['id'])
    if not ts:
        print("Could not fetch transcript. Skipping.")
        return
        
    # 3. Generate LinkedIn Content
    print("Generating AI content...")
    content = generator.generate_linkedin_content(ts)
    if not content:
        print("AI generation failed.")
        return
        
    # 4. Generate Image
    print("Generating hook image...")
    image_path = os.path.join("backend", "data", f"{video['id']}.png")
    image_gen.create_hook_image(content['image_hook'], image_path)
    
    # 5. Post to LinkedIn
    print("Posting to LinkedIn...")
    success = poster.post_to_linkedin(content['post_content'], image_path)
    
    if success:
        print("Successfully posted to LinkedIn!")
        monitor.mark_video_processed(video['id'])
    else:
        print("Posting failed.")

if __name__ == "__main__":
    run_pipeline()
