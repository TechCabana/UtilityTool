import os
from datetime import datetime

PASSPORT_SIZES = {
    "India": (51, 51),       # mm
    "Netherlands": (35, 45)  # mm
}

def get_passport_size(country):
    return PASSPORT_SIZES.get(country, (35, 45))  # Default: Netherlands size

def generate_rename_pattern(original_name, pattern_type, suffix=""):
    name, ext = os.path.splitext(original_name)
    if pattern_type == "date":
        new_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    elif pattern_type == "regex":
        # Placeholder for regex-based renaming
        new_name = name.replace(" ", "_")
    else:
        new_name = name
    if suffix:
        new_name += f"_{suffix}"
    return f"{new_name}{ext}"
