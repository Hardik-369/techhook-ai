import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_linkedin_content(transcript):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Transform the following YouTube video transcript into a high-engagement LinkedIn post.
    
    TRANSCRIPT:
    {transcript}
    
    GUIDELINES:
    1. Hook first line: Must be controversial or deeply curious.
    2. Format: Short, punchy sentences. One idea per line.
    3. Tone: Intelligent, founder-focused, high engagement (slightly "cringe" but effective).
    4. Structure: Micro-story/Insight -> Emotional framing -> Call to action question.
    5. Include 5 relevant hashtags at the end.
    6. Extraction: Extract a separate 6-7 word "Hook Statement" for an image.
    
    RESPONSE FORMAT:
    Return ONLY a JSON object with two keys:
    "post_content": "The full LinkedIn post text"
    "image_hook": "The 6-7 word hook statement"
    """
    
    try:
        response = model.generate_content(prompt)
        # Handle potential safety filters or empty responses
        if not response.text:
            return None
        
        # Strip potential markdown formatting from JSON response
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_json)
        return data
    except Exception as e:
        print(f"Error generating LinkedIn content: {e}")
        return None

if __name__ == "__main__":
    # Test stub
    pass
