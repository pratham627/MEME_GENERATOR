from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

def generate_meme(image_bytes: bytes, top_text: str, bottom_text: str) -> io.BytesIO:
    # Open the image
    img = Image.open(io.BytesIO(image_bytes))
    
    # Resize if too large (optional, but good for performance)
    max_width = 800
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(img)
    
    # Load font - try Arial, fallback to default
    try:
        # Calculate font size relative to image height
        font_size = int(img.height / 10)
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    def draw_text(text, position_y):
        # Wrap text
        chars_per_line = int(img.width / (font_size * 0.5))
        wrapper = textwrap.TextWrapper(width=chars_per_line)
        word_list = wrapper.wrap(text=text)
        
        # Draw each line
        current_y = position_y
        for line in word_list:
            # Get text size using getbbox
            bbox = draw.textbbox((0, 0), line, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            
            x = (img.width - w) / 2
            
            # Outline
            outline_range = int(font_size / 15)
            for dx in range(-outline_range, outline_range + 1):
                for dy in range(-outline_range, outline_range + 1):
                    draw.text((x + dx, current_y + dy), line, font=font, fill="black")
            
            draw.text((x, current_y), line, font=font, fill="white")
            current_y += h + 5 # Add detailed spacing

    if top_text:
        draw_text(top_text.upper(), 10)
    
    if bottom_text:
        # Calculate height for bottom text
        # Simplification: just put it at the bottom minus some padding
        # A more complex calculating would be needed for wrapped bottom text to ensure it fits.
        # For now, let's start drawing from the bottom-ish up or just give it enough space.
        # To do it properly: calculate total height of wrapped text and subtract from img.height
        
        chars_per_line = int(img.width / (font_size * 0.5))
        wrapper = textwrap.TextWrapper(width=chars_per_line)
        word_list = wrapper.wrap(text=bottom_text.upper())
        
        # Calculate total height
        total_text_height = 0
        for line in word_list:
             bbox = draw.textbbox((0, 0), line, font=font)
             h = bbox[3] - bbox[1]
             total_text_height += h + 5
             
        start_y = img.height - total_text_height - 20
        draw_text(bottom_text.upper(), start_y)

    # Save to buffer
    output_buffer = io.BytesIO()
    img.save(output_buffer, format=img.format if img.format else 'JPEG')
    output_buffer.seek(0)
    return output_buffer
