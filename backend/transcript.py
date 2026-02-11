from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_transcript(video_id):
    try:
        # Create an instance to call fetch
        api = YouTubeTranscriptApi()
        # Try to fetch in English (including auto-generated)
        transcript_list = api.list(video_id)
        
        # Look for English (en) or variations like en-US
        transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        data = transcript.fetch()
        
        text = " ".join([t['text'] for t in data])
        return clean_text(text)
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None

def clean_text(text):
    # Remove filler words and clean whitespace
    fillers = [r'\bah\b', r'\buh\b', r'\bum\b', r'\blike\b', r'\byou know\b', r'\bi mean\b']
    for filler in fillers:
        text = re.sub(filler, '', text, flags=re.IGNORECASE)
    
    # Clean multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

if __name__ == "__main__":
    # Test with a known video ID if needed
    pass
