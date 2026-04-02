import os
import glob
import re
import json
import easyocr

def recognize_text(path,out_path):
    """
    Perform OCR text recognition:
    - Skip Checkbox images
    - Skip TableHeader/TableData (these are handled separately)
    - Save extracted text into a JSON structure
    """
    reader = easyocr.Reader(['en'])
    extracted_data = {}
    print(path)
    for image_path in path:
        print(image_path)
        filename = os.path.basename(image_path)
        key_name = os.path.splitext(filename)[0]

        # Skip checkbox and table-related images
        if "Checkbox" in key_name or "TableHeader" in key_name or "TableData" in key_name:
            continue

        # Clean base name (remove trailing _123 if any)
        base_name = re.sub(r'_\d+$', '', key_name)

        result = reader.readtext(image_path, detail=0)
        extracted_text = " ".join(result)

        if base_name not in extracted_data:
            extracted_data[base_name] = []
        extracted_data[base_name].append(extracted_text)

    # Save output JSON
    # output_json = '../Output/JSON/ExtractedText.json'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print(f"[✓] OCR text saved at: {out_path}")
    return f"OCR data structured and saved to {out_path}"
