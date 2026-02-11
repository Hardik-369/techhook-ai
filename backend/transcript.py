from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t['text'] for t in transcript_list])
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
