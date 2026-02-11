from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import speech_recognition as sr
from pydub import AudioSegment
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
        print(f"Method 1 (API) failed for {video_id}")

    # Method 2: Manual Scraper (Custom "youtubetotranscript.com" style)
    try:
        data = scraper.scrape_transcript(video_id)
        if data:
            return clean_text(" ".join([t['text'] for t in data]))
    except Exception as e:
        print(f"Method 2 (Scraper) failed for {video_id}")

    # Method 3: pytube caption extraction
    try:
        yt = YouTube(f"https://youtube.com/watch?v={video_id}")
        caption = yt.captions.get_by_language_code('en') or \
                  yt.captions.get_by_language_code('a.en')
        if caption:
            return clean_text(caption.generate_srt_captions())
    except Exception as e:
        print(f"Method 3 (Pytube) failed for {video_id}")

    # Method 4: Local Speech Recognition (The "Speech to Text" way)
    try:
        audio_path = get_audio_content(video_id)
        if audio_path:
            text = get_transcript_via_local_stt(audio_path)
            # Cleanup
            try: os.remove(audio_path)
            except: pass
            if text:
                return clean_text(text)
    except Exception as e:
        print(f"Method 4 (SpeechRec) failed for {video_id}: {e}")

    return None

def get_transcript_via_local_stt(audio_path):
    """
    Uses SpeechRecognition to extract text from an audio file.
    Converts to wav first for compatibility.
    """
    try:
        # Convert to WAV
        print(f"Converting {audio_path} to WAV...")
        wav_path = audio_path.replace(".mp3", ".wav")
        audio = AudioSegment.from_file(audio_path)
        audio.export(wav_path, format="wav")
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            print("Reading audio file...")
            audio_data = recognizer.record(source)
            print("Performing Speech-to-Text...")
            # Use Google's free Web Speech API
            text = recognizer.recognize_google(audio_data)
            
        # Cleanup WAV
        try: os.remove(wav_path)
        except: pass
        
        return text
    except Exception as e:
        print(f"Local STT error: {e}")
        return None

def get_audio_content(video_id):
    """
    Downloads the audio of a video using pytube.
    """
    try:
        yt = YouTube(f"https://youtube.com/watch?v={video_id}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        # Save as mp3 initially
        out_file = audio_stream.download(output_path="backend/data", filename=f"{video_id}_temp")
        new_file = os.path.join("backend/data", f"{video_id}_audio.mp3")
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
