from PIL import Image
from io import BytesIO
import os

# Standard, practical sizes. Pixels are computed at 300 DPI when mm/in given.
STANDARD_SIZES = {
    # Passport / ID photos
    "Passport – India (51×51 mm)": {"mm": (51, 51), "dpi": 300},
    "Passport – Netherlands (35×45 mm)": {"mm": (35, 45), "dpi": 300},
    "Passport – ICAO (35×45 mm)": {"mm": (35, 45), "dpi": 300},

    # Common prints
    "Photo 4×6 in": {"in": (4, 6), "dpi": 300},
    "Photo 5×7 in": {"in": (5, 7), "dpi": 300},

    # Paper
    "A4 (210×297 mm)": {"mm": (210, 297), "dpi": 300},
    "A5 (148×210 mm)": {"mm": (148, 210), "dpi": 300},

    # Social
    "Instagram Post (1080×1080 px)": {"px": (1080, 1080)},
    "YouTube Thumbnail (1280×720 px)": {"px": (1280, 720)},
}

def mm_to_px(mm_w, mm_h, dpi=300):
    inch_w = mm_w / 25.4
    inch_h = mm_h / 25.4
    return int(round(inch_w * dpi)), int(round(inch_h * dpi))

def inches_to_px(in_w, in_h, dpi=300):
    return int(round(in_w * dpi)), int(round(in_h * dpi))

def target_dims_from_preset(preset_key):
    item = STANDARD_SIZES.get(preset_key)
    if not item:
        return None
    if "px" in item:
        return item["px"]
    if "mm" in item:
        w, h = item["mm"]
        dpi = item.get("dpi", 300)
        return mm_to_px(w, h, dpi)
    if "in" in item:
        w, h = item["in"]
        dpi = item.get("dpi", 300)
        return inches_to_px(w, h, dpi)
    return None

def estimate_compressed_size(image_path, fmt="JPEG", quality=85, subsampling="keep"):
    """
    Return (estimated_bytes, ratio_vs_original).
    Uses an in-memory save to approximate final size.
    """
    try:
        img = Image.open(image_path)
        save_kwargs = {}
        if fmt.upper() == "JPEG":
            # JPEG doesn't support alpha; convert to RGB
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            save_kwargs["quality"] = int(quality)
            save_kwargs["optimize"] = True
            if subsampling != "keep":
                save_kwargs["subsampling"] = subsampling  # 0,1,2 acceptable for PIL
        bio = BytesIO()
        img.save(bio, fmt.upper(), **save_kwargs)
        est_bytes = bio.getvalue()
        orig = os.path.getsize(image_path)
        ratio = (len(est_bytes) / orig) if orig else 1.0
        return len(est_bytes), ratio
    except Exception:
        return None, None

def convert_resize_compress(image_path, out_fmt="JPEG", out_path=None, size=None, keep_aspect=True, quality=85):
    """
    Convert with optional resize and compression. Returns output path.
    - size: (w, h) px if provided
    - keep_aspect True => thumbnail; False => exact resize
    """
    img = Image.open(image_path)
    if size:
        w, h = size
        if keep_aspect:
            img.thumbnail((w, h))
        else:
            img = img.resize((w, h))
    if out_fmt.upper() == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    if out_path is None:
        base, _ = os.path.splitext(image_path)
        out_path = f"{base}_out.{out_fmt.lower()}"
    save_kwargs = {}
    if out_fmt.upper() == "JPEG":
        save_kwargs.update(dict(quality=int(quality), optimize=True))
    img.save(out_path, out_fmt.upper(), **save_kwargs)
    return out_path
