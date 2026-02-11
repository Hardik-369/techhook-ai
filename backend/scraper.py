import requests
import re
import json
import html

def scrape_transcript(video_id):
    """
    Manually scrapes YouTube's internal caption tracks from the page source.
    Returns a list of transcript segments if found, else None.
    """
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15)
        
        # Find ytInitialPlayerResponse
        pattern = r"var ytInitialPlayerResponse = (\{.*?\});"
        match = re.search(pattern, r.text)
        if not match:
            return None
            
        player_response = json.loads(match.group(1))
        captions = player_response.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
        
        if not captions:
            return None
            
        # Prioritize English, then take the first available
        target_track = None
        for track in captions:
            if 'en' in track.get('languageCode', ''):
                target_track = track
                break
        
        if not target_track:
            target_track = captions[0]
            
        track_url = target_track.get("baseUrl")
        if not track_url:
            return None
            
        # Fetch the actual XML/JSON transcript
        # Adding &fmt=json to get JSON format if possible, otherwise it's XML
        track_res = requests.get(track_url + "&fmt=json", timeout=10)
        transcript_data = track_res.json()
        
        segments = []
        for event in transcript_data.get("events", []):
            if "segs" in event:
                text = "".join([s.get("utf8", "") for s in event["segs"]])
                if text.strip():
                    segments.append({"text": html.unescape(text)})
                    
        return segments if segments else None
        
    except Exception as e:
        print(f"Manual scraping failed for {video_id}: {e}")
        return None

if __name__ == "__main__":
    # Test
    res = scrape_transcript("dQw4w9WgXcQ")
    if res:
        print(f"Successfully scraped {len(res)} segments.")
    else:
        print("Scraping failed.")
