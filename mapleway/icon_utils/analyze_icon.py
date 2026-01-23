from PIL import Image
from collections import Counter

def get_dominant_colors(image_path, num_colors=5):
    try:
        image = Image.open(image_path)
        image = image.convert('RGB')
        # Resize for faster processing
        image = image.resize((150, 150))
        pixels = list(image.getdata())
        counts = Counter(pixels)
        common = counts.most_common(num_colors)
        
        print(f"Analysis for: {image_path}")
        print("-" * 30)
        for color, count in common:
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            print(f"Color: {hex_color} (RGB: {color}) - Count: {count}")
            
    except Exception as e:
        print(f"Error analyzing image: {e}")

if __name__ == "__main__":
    icon_path = r"D:\Dev-Env\Antigravity_Projects\mapleway\logo_selection\logo_web_extension_mapleway.png"
    get_dominant_colors(icon_path)
