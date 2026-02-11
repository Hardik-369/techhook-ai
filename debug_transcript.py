from youtube_transcript_api import YouTubeTranscriptApi
import sys

def test_fetch(video_id):
    try:
        api = YouTubeTranscriptApi()
        print(f"Fetching transcript list for {video_id}...")
        transcript_list = api.list(video_id)
        
        print("Available transcripts:")
        for t in transcript_list:
            print(f"- {t.language} ({t.language_code}) [Generated: {t.is_generated}]")
            
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
            print(f"Found English transcript: {transcript.language_code}")
        except:
            print("No English transcript found. Trying translation...")
            first_transcript = next(iter(transcript_list))
            transcript = first_transcript.translate('en')
            print(f"Translated from {first_transcript.language_code} to en")
            
        data = transcript.fetch()
        print(f"Success! Fetched {len(data)} lines.")
        return True
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    test_fetch("A7hPxTmC2SM")
