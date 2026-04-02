# import os
# import cv2
# import numpy as np
# import easyocr
# import glob
# import json
# import re
# from pathlib import Path
# from typing import List, Dict, Optional, Union

# # Initialize EasyOCR reader once
# def get_reader() -> easyocr.Reader:
#     return easyocr.Reader(['en'], gpu=False)

# reader = get_reader()


# def detect_form_checkboxes_checked(
#     image_path: str,
#     size_range: tuple[int,int] = (30, 80),
#     shape_tolerance: float = 0.8,
#     fill_threshold: float = 0.3
# ) -> List[Dict[str, Union[str, bool, float, List[int]]]]:
#     """
#     Detect checkbox boxes in a form patch, compute fill, OCR full sentence.
#     Returns list of entries:
#       {'text': str, 'checked': bool, 'fill_ratio': float, 'box': [x,y,w,h]}
#     """
#     img = cv2.imread(image_path)
#     if img is None:
#         raise FileNotFoundError(f"Couldn’t load {image_path}")
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     H, W = gray.shape

#     # Threshold + clean
#     _, bw = cv2.threshold(gray, 0, 255,
#                           cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE,
#                           cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
#     cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL,
#                                cv2.CHAIN_APPROX_SIMPLE)

#     results = []
#     for c in cnts:
#         x,y,w,h = cv2.boundingRect(c)
#         if not (size_range[0] < w < size_range[1] and size_range[0] < h < size_range[1]):
#             continue
#         peri = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.03*peri, True)
#         if len(approx) != 4:
#             continue
#         pad = int(min(w,h)*0.2)
#         inner = bw[y+pad:y+h-pad, x+pad:x+w-pad]
#         fill = np.count_nonzero(inner)/inner.size
#         checked = fill > fill_threshold
#         # OCR full sentence region
#         roi = img[max(0,y-5):min(H,y+h+5), 0:min(W, x+w+200)]
#         texts = reader.readtext(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB), detail=0)
#         text = " ".join(texts).strip()
#         results.append({'text': text, 'checked': checked, 'fill_ratio': round(fill,2), 'box': [x,y,w,h]})
#     return results


# def extract_all_checkboxes(
#     segmented_root: str,
#     json_path: str,
#     output_json: Optional[str] = None
# ) -> None:
#     """
#     Scan for Checkbox*.jpg under segmented_root,
#     detect checkbox entries, group per question,
#     map each question to its checked answer,
#     and update JSON 'Checkbox' key with that map.
#     """
#     if output_json is None:
#         output_json = json_path

#     data = {}
#     if os.path.exists(json_path):
#         with open(json_path, 'r') as jf:
#             data = json.load(jf)

#     pattern = os.path.join(segmented_root, '*', '*', 'Checkbox*.jpg')
#     imgs = glob.glob(pattern, recursive=True)
#     print(len(imgs))
#     all_entries = []
#     for img_path in imgs:
#         all_entries.extend(detect_form_checkboxes_checked(img_path))

#     # Group by question text (prefix before option)
#     questions: Dict[str, List[Dict]] = {}
#     for e in all_entries:
#         m = re.match(r"(.+?)\s+(Yes|No|NA|NAN?)\b", e['text'])
#         if m:
#             q = m.group(1).strip().rstrip('?') + '?'
#         else:
#             q = e['text']
#         questions.setdefault(q, []).append(e)

#     # Map each question to its checked answer
#     mapping: Dict[str, str] = {}
#     for q, group in questions.items():
#         sel = next((g for g in group if g['checked']), None)
#         if sel:
#             # try regex match first
#             m2 = re.search(r"\b(Yes|No|NA|NAN?)$", sel['text'])
#             if m2:
#                 ans = m2.group(1)
#             else:
#                 # fallback: use box x-order
#                 sorted_grp = sorted(group, key=lambda x: x['box'][0])
#                 idx = sorted_grp.index(sel)
#                 opts = ['Yes', 'No', 'NA']
#                 ans = opts[idx] if idx < len(opts) else ''
#         else:
#             ans = ''
#         mapping[q] = ans

#     # Update JSON and write
#     data['Checkbox'] = mapping
#     os.makedirs(os.path.dirname(output_json), exist_ok=True)
#     with open(output_json, 'w') as jf:
#         json.dump(data, jf, indent=4)

#     # Print mapping
#     for q,a in mapping.items():
#         print(f"\"{q}\": \"{a}\"")

# # Note: imported by main.py; not executable as script
import os
import cv2
import numpy as np
import easyocr
import glob
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Union

# Initialize EasyOCR reader once
def get_reader() -> easyocr.Reader:
    return easyocr.Reader(['en'], gpu=False)

reader = get_reader()


def detect_form_checkboxes_checked(
    image_path: str,
    size_range: tuple[int,int] = (30, 80),
    shape_tolerance: float = 0.8,
    fill_threshold: float = 0.3
) -> List[Dict[str, Union[str, bool, float, List[int]]]]:
    """
    Detect checkbox boxes in a form patch, compute fill, OCR full sentence.
    Returns list of entries:
      {'text': str, 'checked': bool, 'fill_ratio': float, 'box': [x,y,w,h]}
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Couldn’t load {image_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape

    # Threshold + clean
    _, bw = cv2.threshold(gray, 0, 255,
                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE,
                          cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
    cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

    results = []
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if not (size_range[0] < w < size_range[1] and size_range[0] < h < size_range[1]):
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03*peri, True)
        if len(approx) != 4:
            continue
        pad = int(min(w,h)*0.2)
        inner = bw[y+pad:y+h-pad, x+pad:x+w-pad]
        fill = np.count_nonzero(inner)/inner.size
        checked = fill > fill_threshold

        # OCR full sentence region
        roi = img[max(0,y-5):min(H,y+h+5), 0:min(W, x+w+200)]
        texts = reader.readtext(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB), detail=0)
        text = " ".join(texts).strip()
        results.append({'text': text, 'checked': checked, 'fill_ratio': round(fill,2), 'box': [x,y,w,h]})
    return results


def extract_all_checkboxes(
    segmented_root: Optional[str] = None,
    json_path: str = None,
    image_paths: Optional[List[str]] = None,
    output_json: Optional[str] = None
) -> None:
    """
    Either pass a list of checkbox image paths via image_paths,
    or provide segmented_root to glob for them.
    Updates JSON at json_path by merging a mapping under 'Checkbox'.
    """
    if output_json is None:
        output_json = json_path

    # Load existing JSON
    data = {}
    if json_path and os.path.exists(json_path):
        with open(json_path, 'r') as jf:
            try:
                data = json.load(jf)
            except json.JSONDecodeError:
                data = {}

    # Gather all checkbox images
    if image_paths is None:
        if not segmented_root:
            raise ValueError("Must provide either segmented_root or image_paths")
        pattern = os.path.join(segmented_root, '*', '*', 'Checkbox*.jpg')
        image_paths = glob.glob(pattern, recursive=True)

    if not image_paths:
        print("[!] No Checkbox images found.")
        data['Checkbox'] = {}
        with open(output_json, 'w') as jf:
            json.dump(data, jf, indent=4)
        return

    # Run detection on every image
    all_entries = []
    for img_path in image_paths:
        try:
            entries = detect_form_checkboxes_checked(img_path)
            all_entries.extend(entries)
        except Exception as e:
            print(f"[!] Error processing {img_path}: {e}")

    # Group by question prefix
    questions: Dict[str, List[Dict]] = {}
    for e in all_entries:
        m = re.match(r"(.+?)\s+(Yes|No|NA|NAN?)\b", e['text'])
        q = (m.group(1).strip().rstrip('?') + '?') if m else e['text']
        questions.setdefault(q, []).append(e)

    # Map each question to its checked answer
    mapping: Dict[str, str] = {}
    for q, group in questions.items():
        sel = next((g for g in group if g['checked']), None)
        if sel:
            m2 = re.search(r"\b(Yes|No|NA|NAN?)$", sel['text'])
            if m2:
                ans = m2.group(1)
            else:
                sorted_grp = sorted(group, key=lambda x: x['box'][0])
                idx = sorted_grp.index(sel)
                opts = ['Yes', 'No', 'NA']
                ans = opts[idx] if idx < len(opts) else ''
        else:
            ans = ''
        mapping[q] = ans

    # Merge and write
    data['Checkbox'] = mapping
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, 'w') as jf:
        json.dump(data, jf, indent=4)

    # Print mapping
    for q,a in mapping.items():
        print(f"\"{q}\": \"{a}\"")

# Note: imported by main.py; not executable as script
