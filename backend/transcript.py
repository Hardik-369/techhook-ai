from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import google.generativeai as genai
import os
import time
import re
import scraper

def get_transcript(video_id):
    # Method 1: youtube-transcript-api (Fastest)
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        data = transcript.fetch()
        return clean_text(" ".join([t['text'] for t in data]))
    except Exception as e:
        print(f"Primary API failed for {video_id}")

    # Method 2: Manual Scraper
    try:
        data = scraper.scrape_transcript(video_id)
        if data:
            return clean_text(" ".join([t['text'] for t in data]))
    except Exception as e:
        print(f"Manual scraper failed for {video_id}")

    # Method 3: pytube caption extraction
    try:
        yt = YouTube(f"https://youtube.com/watch?v={video_id}")
        caption = yt.captions.get_by_language_code('en') or \
                  yt.captions.get_by_language_code('a.en')
        if caption:
            return clean_text(caption.generate_srt_captions())
    except Exception as e:
        print(f"Pytube captions failed for {video_id}")

    return None

def get_audio_content(video_id):
    """
    Downloads the audio of a video using pytube.
    This can be used for Gemini Multimodal analysis (STT).
    """
    try:
        yt = YouTube(f"https://youtube.com/watch?v={video_id}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        out_file = audio_stream.download(output_path="backend/data", filename=f"{video_id}_audio")
        # Rename to include proper extension
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        if os.path.exists(new_file): os.remove(new_file)
        os.rename(out_file, new_file)
        return new_file
    except Exception as e:
        print(f"Audio download failed for {video_id}: {e}")
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
