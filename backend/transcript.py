from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # 1. Try to find manually created English
        # 2. Try to find generated English
        # 3. Try to find any transcript and translate it
        
        try:
            # Find any English transcript
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        except:
            # If no English, take the first available and translate to English
            first_transcript = next(iter(transcript_list))
            transcript = first_transcript.translate('en')
            
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
