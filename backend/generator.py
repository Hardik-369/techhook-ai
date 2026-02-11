import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_linkedin_content(transcript=None, video_title=None, description=None):
    # Use gemini-flash-latest for stable performance and quota
    model = genai.GenerativeModel('gemini-flash-latest')
    
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
        text = response.text.strip()
        print(f"AI Response received. Length: {len(text)}")
        
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        # Ensure we only have the JSON object
        if "{" in text and "}" in text:
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
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Raw Response snippet: {response.text[:200]}...")
        return None

if __name__ == "__main__":
    # Test stub
    pass
