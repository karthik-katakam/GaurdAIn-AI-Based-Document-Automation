# # import os
# # import glob
# # import json
# # import cv2
# # import easyocr
# # import pandas as pd
# # from typing import List, Optional
# # import re

# # def extract_table(
# #     image_folder: str,
# #     output_json_path: str
# # ) -> None:
# #     """
# #     Scans for *TableData*.png in image_folder,
# #     Groups OCR text into rows based on a fixed 3-column structure,
# #     and emits both CSV & JSON with default headers.

# #     This bypasses header OCR for more reliable extraction.
# #     """
# #     reader = easyocr.Reader(['en'], gpu=False)
# #     rows: List[List[str]] = []

# #     # Use fixed default headers for Schedule A Income
# #     headers = [
# #         "Source of Income (e.g. employment, social security)",
# #         "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
# #         "Total Income Amount"
# #     ]
# #     col_count = len(headers)
# #     print(f"[i] Using default headers ({col_count} cols): {headers}")

# #     # Process all TableData images
# #     data_paths = sorted(glob.glob(os.path.join(image_folder, '*TableData*.png')))
# #     if not data_paths:
# #         print(f"[!] No TableData images found in {image_folder}")
# #         return

# #     for dp in data_paths:
# #         img = cv2.imread(dp, cv2.IMREAD_GRAYSCALE)
# #         if img is None:
# #             print(f"[!] Could not read data: {dp}")
# #             continue
# #         # If background is black (table lines white), invert to white bg, black text
# #         if img.mean() < 127:
# #             img = cv2.bitwise_not(img)
# #         thresh = cv2.adaptiveThreshold(
# #             img, 255,
# #             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
# #             cv2.THRESH_BINARY,
# #             11, 2
# #         )
# #         ocr_results = reader.readtext(thresh, detail=1)
# #         # filter out stray single-digit or header-like tokens
# #         # OCR tokens and remove only single-digit row numbers (keep multi-digit amounts)
# #         ocr_tokens = [t[1].strip() for t in ocr_results]
# #         # Drop pure single-digit tokens (row indices 1-9), but keep multi-digit numbers
# #         filtered = [tok for tok in ocr_tokens if not (tok.isdigit() and len(tok)==1)]

# #         # group into 3-column rows, merging middle if extra
# #         i = 0
# #         while i < len(filtered):
# #             remaining = len(filtered) - i
# #             if remaining == 4:
# #                 # merge 2 middle cells into description
# #                 row = [
# #                     filtered[i],
# #                     filtered[i+1] + ' ' + filtered[i+2],
# #                     filtered[i+3]
# #                 ]
# #                 rows.append(row)
# #                 break
# #             chunk = filtered[i:i+3]
# #             if len(chunk) == 3:
# #                 rows.append(chunk)
# #             else:
# #                 # include incomplete chunk by padding empty strings
# #                 padded = chunk + [''] * (col_count - len(chunk))
# #                 rows.append(padded)
# #                 print(f"[i] Included incomplete chunk: {chunk} padded to {padded}")
# #             i += 3

# #     if not rows:
# #         print("[!] No valid rows extracted.")
# #         return

# #     # Save to DataFrame
# #     df = pd.DataFrame(rows, columns=headers)
# #     os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

# #     # CSV
# #     csv_path = output_json_path.replace('.json', '.csv')
# #     df.to_csv(csv_path, index=False)
# #     print(f"[✓] Table saved to CSV: {csv_path}")

# #     # JSON
# #     records = df.to_dict(orient='records')
# #     with open(output_json_path, 'w') as jf:
# #         json.dump({'ExtractedTable': records}, jf, indent=4)
# #     print(f"[✓] Table saved to JSON: {output_json_path}")

# import os
# import glob
# import json
# import cv2
# import easyocr
# import pandas as pd
# from typing import List, Optional
# import re


# def extract_table(
#     image_folder: str,
#     output_json_path: str
# ) -> None:
#     """
#     Scans for *TableHeader*.png and *TableData*.png in image_folder,
#     Uses hardcoded headers based on Schedule_A or Schedule_B file prefixes,
#     Groups OCR text into rows, and emits CSV & JSON.
#     """
#     reader = easyocr.Reader(['en'], gpu=False)
#     # 1) Determine table type by header filename
#     header_paths = sorted(glob.glob(os.path.join(image_folder, '*TableHeader*.png')))
#     if header_paths:
#         header_name = os.path.basename(header_paths[0])
#         if 'Schedule_A' in header_name:
#             headers = [
#                 "Source of Income (e.g. employment, social security)",
#                 "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
#                 "Total Income Amount"
#             ]
#         elif 'Schedule_B' in header_name:
#             headers = [
#                 "Category",
#                 "Payment Date/Period",
#                 "Payee",
#                 "Amount Spent"
#             ]
#         else:
#             # fallback to A
#             headers = [
#                 "Source of Income (e.g. employment, social security)",
#                 "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
#                 "Total Income Amount"
#             ]
#     else:
#         print(f"[!] No TableHeader found in {image_folder}, defaulting to Schedule A headers.")
#         headers = [
#             "Source of Income (e.g. employment, social security)",
#             "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
#             "Total Income Amount"
#         ]

#     col_count = len(headers)
#     print(f"[i] Using headers ({col_count} cols): {headers}")

#     # 2) Process data images
#     rows: List[List[str]] = []
#     data_paths = sorted(glob.glob(os.path.join(image_folder, '*TableData*.png')))
#     if not data_paths:
#         print(f"[!] No TableData images found in {image_folder}")
#         return

#     for dp in data_paths:
#         img = cv2.imread(dp, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             print(f"[!] Could not read data: {dp}")
#             continue
#         # invert if dark background
#         if img.mean() < 127:
#             img = cv2.bitwise_not(img)
#         thresh = cv2.adaptiveThreshold(
#             img, 255,
#             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#             cv2.THRESH_BINARY,
#             11, 2
#         )
#         ocr_results = reader.readtext(thresh, detail=1)
#         tokens = [t[1].strip() for t in ocr_results]
#         # drop row index numbers (single digits)
#         filtered = [tok for tok in tokens if not (tok.isdigit() and len(tok)==1)]

#         # group tokens into rows of length col_count, merging if extra
#         i = 0
#         while i < len(filtered):
#             rem = len(filtered) - i
#             if col_count == 3 and rem == 4:
#                 row = [
#                     filtered[i],
#                     filtered[i+1] + ' ' + filtered[i+2],
#                     filtered[i+3]
#                 ]
#                 rows.append(row)
#                 break
#             chunk = filtered[i:i+col_count]
#             if len(chunk) == col_count:
#                 rows.append(chunk)
#             else:
#                 # pad incomplete row
#                 padded = chunk + [''] * (col_count - len(chunk))
#                 rows.append(padded)
#                 print(f"[i] Padded incomplete row: {chunk} -> {padded}")
#             i += col_count

#     if not rows:
#         print("[!] No valid rows extracted.")
#         return

#     # 3) Save outputs
#     df = pd.DataFrame(rows, columns=headers)
#     os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

#     csv_path = output_json_path.replace('.json', '.csv')
#     df.to_csv(csv_path, index=False)
#     print(f"[✓] Table saved to CSV: {csv_path}")

#     records = df.to_dict(orient='records')
#     with open(output_json_path, 'w') as jf:
#         json.dump({'ExtractedTable': records}, jf, indent=4)
#     print(f"[✓] Table saved to JSON: {output_json_path}")

# import os
# import glob
# import json
# import cv2
# import easyocr
# import pandas as pd
# from typing import List, Optional
# import re


# def extract_table(
#     image_folder: str,
#     output_json_path: str
# ) -> None:
#     """
#     Scans for *TableHeader*.png and *TableData*.png in image_folder,
#     Uses hardcoded headers based on Schedule_A or Schedule_B file prefixes,
#     Groups OCR text into rows, and emits CSV & JSON.
#     """
#     reader = easyocr.Reader(['en'], gpu=False)
#     # 1) Determine table type by header filename
#     header_paths = sorted(glob.glob(os.path.join(image_folder, '*TableHeader*.png')))
#     if header_paths:
#         header_name = os.path.basename(header_paths[0])
#         if 'Schedule_A' in header_name:
#             headers = [
#                 "Source of Income (e.g. employment, social security)",
#                 "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
#                 "Total Income Amount"
#             ]
#         elif 'Schedule_B' in header_name:
#             headers = [
#                 "Category",
#                 "Payment Date/Period",
#                 "Payee",
#                 "Amount Spent"
#             ]
#         else:
#             # fallback to A
#             headers = [
#                 "Source of Income (e.g. employment, social security)",
#                 "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
#                 "Total Income Amount"
#             ]
#     else:
#         print(f"[!] No TableHeader found in {image_folder}, defaulting to Schedule A headers.")
#         headers = [
#             "Source of Income (e.g. employment, social security)",
#             "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
#             "Total Income Amount"
#         ]

#     col_count = len(headers)
#     print(f"[i] Using headers ({col_count} cols): {headers}")

#     # 2) Process data images
#     rows: List[List[str]] = []
#     data_paths = sorted(glob.glob(os.path.join(image_folder, '*TableData*.png')))
#     if not data_paths:
#         print(f"[!] No TableData images found in {image_folder}")
#         return

#     for dp in data_paths:
#         img = cv2.imread(dp, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             print(f"[!] Could not read data: {dp}")
#             continue
#         # invert if dark background
#         if img.mean() < 127:
#             img = cv2.bitwise_not(img)
#         thresh = cv2.adaptiveThreshold(
#             img, 255,
#             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#             cv2.THRESH_BINARY,
#             11, 2
#         )
#         ocr_results = reader.readtext(thresh, detail=1)
#         tokens = [t[1].strip() for t in ocr_results]
#         # drop row index numbers (single digits)
#         filtered = [tok for tok in tokens if not (tok.isdigit() and len(tok)==1)]

#         # group tokens into rows of length col_count, merging if extra
#         i = 0
#         while i < len(filtered):
#             rem = len(filtered) - i
#             if col_count == 3 and rem == 4:
#                 row = [
#                     filtered[i],
#                     filtered[i+1] + ' ' + filtered[i+2],
#                     filtered[i+3]
#                 ]
#                 rows.append(row)
#                 break
#             chunk = filtered[i:i+col_count]
#             if len(chunk) == col_count:
#                 rows.append(chunk)
#             else:
#                 # pad incomplete row
#                 padded = chunk + [''] * (col_count - len(chunk))
#                 rows.append(padded)
#                 print(f"[i] Padded incomplete row: {chunk} -> {padded}")
#             i += col_count

#     if not rows:
#         print("[!] No valid rows extracted.")
#         return

#         # 3) Save outputs
#     df = pd.DataFrame(rows, columns=headers)
#     os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

#     # Save CSV
#     csv_path = output_json_path.replace('.json', '.csv')
#     df.to_csv(csv_path, index=False)
#     print(f"[✓] Table saved to CSV: {csv_path}")

#     # Merge into existing JSON
#     records = df.to_dict(orient='records')
#     # Load existing JSON data if present
#     if os.path.exists(output_json_path):
#         with open(output_json_path, 'r') as jf:
#             try:
#                 data = json.load(jf)
#             except json.JSONDecodeError:
#                 data = {}
#     else:
#         data = {}
#     # Update only the table section
#     data['ExtractedTable'] = records
#     # Write back full JSON
#     with open(output_json_path, 'w') as jf:
#         json.dump(data, jf, indent=4)
#     print(f"[✓] Table merged into JSON: {output_json_path}")

import os
import glob
import json
import cv2
import easyocr
import pandas as pd
from typing import List, Optional


def extract_table(
    image_folder: str,
    output_json_path: str
) -> None:
    """
    Scans for Schedule_A and Schedule_B table header/data images in image_folder,
    extracts both tables into separate CSVs and merges both into JSON under keys
    'Schedule_A' and 'Schedule_B'.
    """
    reader = easyocr.Reader(['en'], gpu=False)

    # Prepare output container
    combined_data: dict = {}
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Iterate over both schedule types
    for schedule in ('Schedule_A', 'Schedule_B'):
        # Determine headers based on schedule
        if schedule == 'Schedule_A':
            headers = [
                "Source of Income (e.g. employment, social security)",
                "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
                "Total Income Amount"
            ]
        else:
            headers = [
                "Category",
                "Payment Date/Period",
                "Payee",
                "Amount Spent"
            ]
        col_count = len(headers)

        # Find corresponding data images
        data_pattern = os.path.join(image_folder, f'*{schedule}*TableData*.png')
        data_paths = sorted(glob.glob(data_pattern))
        if not data_paths:
            print(f"[!] No data images for {schedule} in {image_folder}")
            continue

        rows: List[List[str]] = []
        for dp in data_paths:
            img = cv2.imread(dp, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"[!] Could not read data: {dp}")
                continue
            # invert if dark background
            if img.mean() < 127:
                img = cv2.bitwise_not(img)
            thresh = cv2.adaptiveThreshold(
                img, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
            ocr_results = reader.readtext(thresh, detail=1)
            tokens = [t[1].strip() for t in ocr_results]
            # drop single-digit row numbers
            filtered = [tok for tok in tokens if not (tok.isdigit() and len(tok) == 1)]

            # chunk into rows
            i = 0
            while i < len(filtered):
                chunk = filtered[i:i+col_count]
                if len(chunk) == col_count:
                    rows.append(chunk)
                else:
                    # pad shorter rows
                    padded = chunk + [''] * (col_count - len(chunk))
                    rows.append(padded)
                    print(f"[i] Padded {schedule} incomplete row: {chunk} -> {padded}")
                i += col_count

        # Create DataFrame and save CSV
        if not rows:
            print(f"[!] No valid rows extracted for {schedule}.")
            continue
        df = pd.DataFrame(rows, columns=headers)
        csv_path = output_json_path.replace('.json', f'_{schedule}.csv')
        df.to_csv(csv_path, index=False)
        print(f"[✓] {schedule} table saved to {csv_path}")

        # Merge into combined JSON
        combined_data[schedule] = df.to_dict(orient='records')

    # Load existing JSON if exists
    if os.path.exists(output_json_path):
        with open(output_json_path, 'r') as jf:
            try:
                base = json.load(jf)
            except json.JSONDecodeError:
                base = {}
    else:
        base = {}

    # Update base with combined tables
    base.update(combined_data)
    with open(output_json_path, 'w') as jf:
        json.dump(base, jf, indent=4)
    print(f"[✓] All tables merged into JSON: {output_json_path}")
