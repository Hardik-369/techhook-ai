from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

def create_hook_image(text, output_path):
    # Image size
    width, height = 1080, 1080
    
    # Random Gradient Background
    colors = [
        ((20, 20, 20), (60, 60, 60)),   # Dark grey
        ((10, 30, 60), (30, 60, 100)),  # Deep blue
        ((60, 10, 10), (100, 30, 30)),  # Deep red
        ((30, 60, 10), (60, 100, 30)),  # Deep green
    ]
    color_start, color_end = random.choice(colors)
    
    image = Image.new('RGB', (width, height), color_start)
    draw = ImageDraw.Draw(image)
    
    # Simple vertical gradient
    for y in range(height):
        r = int(color_start[0] + (color_end[0] - color_start[0]) * y / height)
        g = int(color_start[1] + (color_end[1] - color_start[1]) * y / height)
        b = int(color_start[2] + (color_end[2] - color_start[2]) * y / height)
        draw.line((0, y, width, y), fill=(r, g, b))

    # Add subtle noise/texture
    for _ in range(5000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        draw.point((x, y), fill=(255, 255, 255, 30))

    # Text wrapping and drawing
    try:
        # Use a bold sans-serif font. Default to Arial or similar if not found.
        # On Windows, Arial is usually at C:\Windows\Fonts\arialbd.ttf
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        if not os.path.exists(font_path):
             font_path = "arial.ttf" # Fallback to whatever is available
        
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Wrap text to 6-7 words usually fits in 2-3 lines
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if len(current_line) >= 3:
            lines.append(" ".join(current_line))
            current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    
    full_text = "\n".join(lines)
    
    # Calculate text position (center)
    # getbbox returns (left, top, right, bottom)
    bbox = draw.multiline_textbbox((0, 0), full_text, font=font, align="center")
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    # Draw shadow
    draw.multiline_text((x+4, y+4), full_text, font=font, fill=(0, 0, 0), align="center")
    # Draw text
    draw.multiline_text((x, y), full_text, font=font, fill=(255, 255, 255), align="center")
    
    image.save(output_path)
    return output_path

if __name__ == "__main__":
    # Test
    # create_hook_image("AI IS REPLACING SMART FOUNDERS", "test_hook.png")
    pass
