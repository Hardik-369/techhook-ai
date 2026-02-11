import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_gen(title, desc):
    model = genai.GenerativeModel('gemini-flash-latest')
    source_material = f"VIDEO TITLE: {title}\n\nVIDEO DESCRIPTION:\n{desc}"
    
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
        print("Sending request to Gemini...")
        response = model.generate_content(prompt)
        print("Raw AI Output:")
        print(response.text)
        
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            text = text[start:end]
            
        data = json.loads(text)
        print("\nParsed Data:")
        print(json.dumps(data, indent=2))
        
    except Exception as e:
        print(f"\nFAILURE: {e}")
        if 'response' in locals() and hasattr(response, 'candidates'):
             print(f"Candidates status: {response.candidates[0].finish_reason if response.candidates else 'No candidates'}")

if __name__ == "__main__":
    title = "I Gave Seedance 2.0 One Photo and It Made Me Talk Like a YouTuber!"
    desc = "Testing new AI tools for creators." 
    test_gen(title, desc)
