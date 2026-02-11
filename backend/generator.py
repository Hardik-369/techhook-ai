import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_from_audio(audio_path, video_title):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # 1. Upload the file to Gemini File API
        print(f"Uploading {audio_path} to Gemini...")
        audio_file = genai.upload_file(path=audio_path)
        
        # 2. Wait for processing (usually instant for audio)
        while audio_file.state.name == "PROCESSING":
            time.sleep(2)
            audio_file = genai.get_file(audio_file.name)
            
        # 3. Generate post
        prompt = f"""
        You are an expert LinkedIn ghostwriter. 
        I am providing the audio from a YouTube video titled: "{video_title}".
        Listen to the audio and create a high-engagement LinkedIn post.
        
        GUIDELINES:
        - Hook first line: Must be controversial or a pattern interrupt.
        - Tone: Intelligent, founder-focused, high engagement.
        - Image Hook: Extract a separate 6-7 word "Hook Statement" for an image overlay.
        
        FORMAT:
        Return ONLY a JSON object with two keys:
        "post_content": "The full LinkedIn post text"
        "image_hook": "The 6-7 word hook statement"
        """
        
        response = model.generate_content([prompt, audio_file])
        
        # Cleanup file from Gemini API (Optional but good practice)
        # genai.delete_file(audio_file.name)
        
        # Robust JSON extraction
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            text = text[start:end]
            
        return json.loads(text)
        
    except Exception as e:
        print(f"Gemini Audio analysis failed: {e}")
        return None

def generate_linkedin_content(transcript=None, video_title=None, description=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Build source material based on what's available
    source_material = ""
    if transcript and len(transcript.strip()) > 100:
        source_material = f"TRANSCRIPT:\n{transcript}"
    elif video_title:
        source_material = f"VIDEO TITLE: {video_title}\n\nVIDEO DESCRIPTION:\n{description if description else 'No description available.'}"
    else:
        print("No valid input for AI generation.")
        return None

    prompt = f"""
    You are an expert LinkedIn ghostwriter. Create a high-engagement post based on the following YouTube video content:
    
    {source_material}
    
    GUIDELINES:
    1. Hook first line: Must be controversial, curious, or a pattern interrupt.
    2. Format: Short, punchy sentences. One idea per line.
    3. Tone: Intelligent, founder-focused, high engagement (slightly "cringe" but effective).
    4. Structure: Insight -> Emotional framing -> Call to action question.
    5. Include 5 relevant hashtags at the end.
    6. Image Hook: Provide a separate 6-7 word "Hook Statement" for an image overlay. It must be bold and provocative.
    
    RESPONSE FORMAT:
    Return ONLY a JSON object with two keys:
    "post_content": "The full LinkedIn post text"
    "image_hook": "The 6-7 word hook statement"
    """
    
    try:
        response = model.generate_content(prompt)
        if not response or not response.text:
            print("Gemini returned an empty response.")
            return None
        
        # Robust JSON extraction
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "{" in text and "}" in text:
            # Try to find the first { and last }
            start = text.find("{")
            end = text.rfind("}") + 1
            text = text[start:end]
            
        data = json.loads(text)
        
        # Validate keys
        if "post_content" in data and "image_hook" in data:
            return data
        else:
            print(f"Missing keys in AI response: {data.keys()}")
            return None
            
    except Exception as e:
        print(f"Error generating LinkedIn content: {e}")
        if 'response' in locals():
            print(f"Raw Response: {response.text[:500]}")
        return None

if __name__ == "__main__":
    # Test stub
    pass
