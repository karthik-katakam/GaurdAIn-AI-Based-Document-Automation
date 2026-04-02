# # File: validators.py
# import re
# from typing import Any, Dict, List


# def parse_amount(s: Any) -> float:
#     """Convert strings like '19,80,98.00' or '1,200' to floats."""
#     if s is None:
#         return 0.0
#     s = str(s).replace("'", "").replace(",", "")
#     nums = re.findall(r"\d+(?:\.\d+)?", s)
#     try:
#         return float(nums[0]) if nums else 0.0
#     except:
#         return 0.0


# def validate_report(data: Dict) -> Dict[str, List[str]]:
#     errors: List[str] = []
#     warnings: List[str] = []

#     # 1. Bond check
#     bond = data.get("Checkbox", {}) \
#                .get("If a bond is required, is one filed that covers this period?", "") \
#                .lower()
#     if bond not in ("yes", "y", "true", "1"):
#         errors.append("Bond is required but not filed.")

#     # 2. Assets traced
#     assets_traced = data.get("Checkbox", {}) \
#                         .get("Have you identified, traced and collected all ofthe incapacitated person  s assets?", "") \
#                         .lower()
#     if assets_traced in ("no", "n", "false", "0"):
#         errors.append("Assets not fully traced (Question B = No).")

#     # 3. Tax returns
#     tax = data.get("Checkbox", {}) \
#               .get("Have all of the incapacitated person's past and current state and federal tax returns?", "") \
#               .lower()
#     if tax in ("no", "n", "false", "0", "n/a"):
#         errors.append("Tax returns not current (Question C = No/N/A).")

#     # 4. Cash‐balance arithmetic
#     beg = parse_amount(data.get("Beginning_Cash_Balance", ["0"])[0])
#     inc = sum(parse_amount(item.get("Total Income Amount")) for item in data.get("Schedule_A", []))
#     dis = sum(parse_amount(item.get("Amount Spent")) for item in data.get("Schedule_B", []))
#     calc_end = beg + inc - dis
#     rep_end = parse_amount(data.get("Ending_Cash_Balance", [""])[0])
#     if abs(calc_end - rep_end) > 0.01:
#         errors.append(f"Ending cash mismatch: calculated {calc_end:.2f} vs reported {rep_end:.2f}.")

#     # 5. Negative or dropping net estate
#     if calc_end < 0:
#         errors.append(f"Ending cash balance negative ({calc_end:.2f}).")
#     if dis > inc:
#         warnings.append(f"Disbursements ({dis:.2f}) exceed income ({inc:.2f}).")

#     # 6. Disbursements vs assets: car bills without car asset
#     all_assets = " ".join(str(v) for sched in ("Schedule_A", "Schedule_B")
#                           for item in data.get(sched, []) for v in item.values()).lower()
#     car_bills = any(
#         kw in item.get("Category", "").lower()
#         for item in data.get("Schedule_B", [])
#         for kw in ("car", "registration", "insurance", "repairs")
#     )
#     if "car" not in all_assets and car_bills:
#         errors.append("Car-related disbursement without a car asset.")

#     # 7. High-value estate bond requirement
#     if calc_end >= 50000 and bond not in ("yes", "y"):
#         errors.append("Net estate ≥ $50K but bond not filed or zero.")

#     # 8. Missing required fields as errors
#     for field in ("DocketNumber", "Date"):
#         values = data.get(field, []) if isinstance(data.get(field), list) else [data.get(field)]
#         if not any(val for val in values if str(val).strip()):
#             errors.append(f"Missing or empty required field: {field}.")
#     # 9. Other metadata fields as warnings
#     for field in ("IncapacitatedPerson", "GaurdianName", "FormName"):
#         values = data.get(field, []) if isinstance(data.get(field), list) else [data.get(field)]
#         if not any(val for val in values if str(val).strip()):
#             warnings.append(f"Missing or empty metadata field: {field}.")

#     # 10. Checkbox consistency
#     q4 = data.get("Checkbox", {}).get(
#         "Has the ownership of the property changed since the inventory or last report?", "").lower()
#     q5 = data.get("Checkbox", {}).get(
#         "Is information Or assistance, whether from the court Or a community agency,?", "").lower()
#     if q4 == "no" and q5 == "yes":
#         warnings.append("Question 4 = No but Question 5 = Yes; check consistency.")

#     # 11. Schedule A–EZ / B–EZ responses
#     if not data.get("SCHEDULE_A-EZ:_Income", [""])[0]:
#         warnings.append("Schedule A–EZ Income missing or zero.")
#     if not data.get("SCHEDULE_B-EZ:_Disbursements", [""])[0]:
#         warnings.append("Schedule B–EZ Disbursements missing or zero.")

#     # 12. Attach well-being docs
#     warnings.append(
#         "Ensure Well-Being or Verified Complaint attachments are present for living-situation checks."
#     )

#     return {"errors": errors, "warnings": warnings}

# # File: main_pipeline.py (unchanged)
# File: validators.py
import re
from typing import Any, Dict, List


def parse_amount(s: Any) -> float:
    """Convert strings like '19,80,98.00' or '1,200' to floats."""
    if s is None:
        return 0.0
    s = str(s).replace("'", "").replace(",", "")
    nums = re.findall(r"\d+(?:\.\d+)?", s)
    try:
        return float(nums[0]) if nums else 0.0
    except:
        return 0.0


def validate_report(data: Dict) -> Dict[str, List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Bond check
    bond = data.get("Checkbox", {}) \
               .get("If a bond is required, is one filed that covers this period?", "") \
               .lower()
    if bond not in ("yes", "y", "true", "1"):
        errors.append("Bond is required but not filed.")

    # 2. Assets traced
    assets_traced = data.get("Checkbox", {}) \
                        .get("Have you identified, traced and collected all ofthe incapacitated person  s assets?", "") \
                        .lower()
    if assets_traced in ("no", "n", "false", "0"):
        errors.append("Assets not fully traced (Question B = No).")

    # 3. Tax returns
    tax = data.get("Checkbox", {}) \
              .get("Have all of the incapacitated person's past and current state and federal tax returns?", "") \
              .lower()
    if tax in ("no", "n", "false", "0", "n/a"):
        errors.append("Tax returns not current (Question C = No/N/A).")

    # 4. Cash-balance arithmetic
    beg = parse_amount(data.get("Beginning_Cash_Balance", ["0"])[0])
    inc = sum(parse_amount(item.get("Total Income Amount")) for item in data.get("Schedule_A", []))
    dis = sum(parse_amount(item.get("Amount Spent")) for item in data.get("Schedule_B", []))
    calc_end = beg + inc - dis
    rep_end = parse_amount(data.get("Ending_Cash_Balance", [""])[0])
    if abs(calc_end - rep_end) > 0.01:
        errors.append(f"Ending cash mismatch: calculated {calc_end:.2f} vs reported {rep_end:.2f}.")

    # 5. Negative or dropping net estate
    if calc_end < 0:
        errors.append(f"Ending cash balance negative ({calc_end:.2f}).")
    if dis > inc:
        warnings.append(f"Disbursements ({dis:.2f}) exceed income ({inc:.2f}).")

    # 6. Disbursements vs assets: car bills without car asset
    all_assets = " ".join(str(v) for sched in ("Schedule_A", "Schedule_B")
                          for item in data.get(sched, []) for v in item.values()).lower()
    car_bills = any(
        kw in item.get("Category", "").lower()
        for item in data.get("Schedule_B", [])
        for kw in ("car", "registration", "insurance", "repairs")
    )
    if "car" not in all_assets and car_bills:
        errors.append("Car-related disbursement without a car asset.")

    # 7. High-value estate bond requirement
    if calc_end >= 50000 and bond not in ("yes", "y"):
        errors.append("Net estate ≥ $50K but bond not filed or zero.")

    # 8. Missing required fields as errors
    for field in ("DocketNumber", "Date"):
        values = data.get(field, []) if isinstance(data.get(field), list) else [data.get(field)]
        if not any(val for val in values if str(val).strip()):
            errors.append(f"Missing or empty required field: {field}.")

    # 9. Other metadata fields as warnings
    for field in ("IncapacitatedPerson", "GaurdianName", "FormName"):
        values = data.get(field, []) if isinstance(data.get(field), list) else [data.get(field)]
        if not any(val for val in values if str(val).strip()):
            warnings.append(f"Missing or empty metadata field: {field}.")

    # 10. Checkbox consistency
    q4 = data.get("Checkbox", {}).get(
        "Has the ownership of the property changed since the inventory or last report?", "").lower()
    q5 = data.get("Checkbox", {}).get(
        "Is information Or assistance, whether from the court Or a community agency,?", "").lower()
    if q4 == "no" and q5 == "yes":
        warnings.append("Question 4 = No but Question 5 = Yes; check consistency.")

    # 11. Schedule A–EZ / B–EZ responses
    if not data.get("SCHEDULE_A-EZ:_Income", [""])[0]:
        warnings.append("Schedule A–EZ Income missing or zero.")
    if not data.get("SCHEDULE_B-EZ:_Disbursements", [""])[0]:
        warnings.append("Schedule B–EZ Disbursements missing or zero.")

    # 12. Incomplete Schedule_A rows as warning
    keys = [
        "Source of Income (e.g. employment, social security)",
        "Description (e.g. 12 months times $ amount, or lump sum of $ amount, etc.)",
        "Total Income Amount"
    ]
    for item in data.get("Schedule_A", []):
        row_vals = [item.get(k, "") for k in keys]
        non_empty = [v for v in row_vals if v and v.strip()]
        if len(non_empty) < len(keys):
            warnings.append(
                f"Padded Schedule_A incomplete row: {non_empty} -> {row_vals}"
            )

    # 13. FormName consistency
    form = data.get("FormName", [""])[0]
    if "Guardianship Report" not in form:
        warnings.append(f"Unexpected FormName: {form}")

    # 14. Date format check
    for dt in data.get("Date", []):
        if dt and not re.match(r"\d{2}-\d{2}-\d{4}", dt):
            warnings.append(f"Date '{dt}' not in DD-MM-YYYY format.")

    # 15. Beginning cash positive
    if beg < 0:
        errors.append(f"Beginning cash balance negative ({beg:.2f}).")

    # 16. Single income entry > beginning cash
    for item in data.get("Schedule_A", []):
        amt = parse_amount(item.get("Total Income Amount"))
        if amt > beg:
            warnings.append(f"Income entry exceeds beginning cash balance: {amt:.2f} > {beg:.2f}.")

    # 17. Disbursements exceed 50% of available funds
    if (beg + inc) > 0 and dis > 0.5 * (beg + inc):
        warnings.append("Disbursements exceed 50% of available funds.")

    # 18. Duplicate entries in Schedule_A
    seen = set()
    for item in data.get("Schedule_A", []):
        key = (
            item.get("Source of Income (e.g. employment, social security)"),
            item.get("Total Income Amount")
        )
        if key in seen:
            warnings.append(f"Duplicate income entry detected: {key}.")
        seen.add(key)

    # 19. All Schedule_B amounts zero or missing
    if data.get("Schedule_B") and all(
        parse_amount(i.get("Amount Spent")) == 0 for i in data.get("Schedule_B", [])
    ):
        warnings.append("All Schedule_B amounts are zero or missing.")

    # 20. Attach well-being docs
    warnings.append(
        "Ensure Well-Being or Verified Complaint attachments are present for living-situation checks."
    )

    return {"errors": errors, "warnings": warnings}

# File: main_pipeline.py (unchanged)
