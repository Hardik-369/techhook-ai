from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import re
import scraper

def get_transcript(video_id):
    # Method 1: youtube-transcript-api (Fastest, uses API)
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        except:
            first_transcript = next(iter(transcript_list))
            transcript = first_transcript.translate('en')
            
        data = transcript.fetch()
        return clean_text(" ".join([t['text'] for t in data]))
    except Exception as e:
        print(f"Primary transcript API failed for {video_id}: {e}")

    # Method 2: Manual Scraper (The "youtubetotranscript.com" way)
    try:
        data = scraper.scrape_transcript(video_id)
        if data:
            return clean_text(" ".join([t['text'] for t in data]))
    except Exception as e:
        print(f"Manual scraper failed for {video_id}: {e}")

    # Method 3: pytube (Scraping fallback)
    try:
        yt = YouTube(f"https://youtube.com/watch?v={video_id}")
        # Try to find English captions
        caption = yt.captions.get_by_language_code('en') or \
                  yt.captions.get_by_language_code('a.en') or \
                  next(iter(yt.captions.all()), None)
        
        if caption:
            return clean_text(caption.generate_srt_captions())
    except Exception as e:
        print(f"Secondary transcript (pytube) failed for {video_id}: {e}")

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
