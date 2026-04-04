# core/utils.py
from datetime import datetime
from io import BytesIO
from PIL import Image

def parse_timestamp(timestamp_str):
    """Parse ISO timestamp string to datetime object"""
    if not timestamp_str:
        return None
    return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

def parse_supabase_data(data, *timestamp_fields):
    """Parse timestamp fields in Supabase response data"""
    if isinstance(data, list):
        return [parse_supabase_data(item, *timestamp_fields) for item in data]
    
    if isinstance(data, dict):
        for field in timestamp_fields:
            if data.get(field):
                data[field] = parse_timestamp(data[field])
    
    return data

def compress_image(image_file, max_size_kb=500):
    img = Image.open(image_file)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    quality = 85
    output = BytesIO()
    
    img.save(output, format='JPEG', quality=quality)
    
    while output.tell() > max_size_kb * 1024 and quality > 10:
        quality -= 5
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality)
    
    while output.tell() > max_size_kb * 1024:
        width, height = img.size
        if width <= 300 or height <= 300:
            break
        img = img.resize((int(width * 0.9), int(height * 0.9)), Image.Resampling.LANCZOS)
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality)
        
    output.seek(0)
    return output