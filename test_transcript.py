from youtube_transcript_api import YouTubeTranscriptApi
import youtube_transcript_api

print(f"Module attributes: {dir(youtube_transcript_api)}")
print(f"Class attributes: {[m for m in dir(YouTubeTranscriptApi) if not m.startswith('_')]}")

try:
    print("Testing get_transcript...")
    t = YouTubeTranscriptApi.get_transcript("A7hPxTmC2SM")
    print("Success with get_transcript!")
except Exception as e:
    print(f"get_transcript failed: {e}")

try:
    print("Testing list_transcripts...")
    l = YouTubeTranscriptApi.list_transcripts("A7hPxTmC2SM")
    print("Success with list_transcripts!")
except Exception as e:
    print(f"list_transcripts failed: {e}")

try:
    print("Testing fetch as static method...")
    f = YouTubeTranscriptApi.fetch("A7hPxTmC2SM")
    print("Success with fetch as static method!")
    print(f[:2]) # Print first 2 entries
except Exception as e:
    print(f"fetch as static failed: {e}")

try:
    print("Testing fetch as instance method...")
    f = YouTubeTranscriptApi().fetch("A7hPxTmC2SM")
    print("Success with fetch as instance method!")
    print(f[:2])
except Exception as e:
    print(f"fetch as instance failed: {e}")

try:
    print("Testing list as static method...")
    l = YouTubeTranscriptApi.list("A7hPxTmC2SM")
    print("Success with list as static method!")
    print(l)
except Exception as e:
    print(f"list as static failed: {e}")

