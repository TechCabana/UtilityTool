import os, re
from datetime import datetime

def format_with_tokens(stem, path, number=None, pad=2, date_source="now"):
    # {date} token
    if "{date}" in stem:
        dt = datetime.now() if date_source == "now" else datetime.fromtimestamp(os.path.getmtime(path))
        stem = stem.replace("{date}", dt.strftime("%Y%m%d"))
    # {num} token
    if "{num}" in stem and number is not None:
        stem = stem.replace("{num}", str(number).zfill(pad))
    return stem

def preview_new_name(path, prefix="", suffix="", number=None, pad=2,
                     date_source="now", regex_find=None, regex_replace=None, case="none"):
    folder, filename = os.path.split(path)
    stem, ext = os.path.splitext(filename)

    # regex find/replace on stem
    if regex_find:
        try:
            stem = re.sub(regex_find, regex_replace or "", stem)
        except re.error:
            pass

    # tokens
    stem = format_with_tokens(stem, path, number=number, pad=pad, date_source=date_source)

    # apply prefix/suffix
    stem = f"{prefix}{stem}{suffix}"

    # case transform
    case = (case or "none").lower()
    if case == "lower": stem = stem.lower()
    elif case == "upper": stem = stem.upper()
    elif case == "title": stem = stem.title()

    return os.path.join(folder, f"{stem}{ext}")

def batch_preview(paths, prefix="", suffix="", start=1, pad=2, date_source="now",
                  regex_find=None, regex_replace=None, case="none", numbering=False):
    previews = []
    counter = start
    for p in paths:
        number = counter if numbering else None
        previews.append(preview_new_name(
            p, prefix=prefix, suffix=suffix, number=number, pad=pad,
            date_source=date_source, regex_find=regex_find, regex_replace=regex_replace, case=case
        ))
        if numbering:
            counter += 1
    return previews

def apply_renames(paths, previews):
    for src, dst in zip(paths, previews):
        if src != dst:
            os.rename(src, dst)
