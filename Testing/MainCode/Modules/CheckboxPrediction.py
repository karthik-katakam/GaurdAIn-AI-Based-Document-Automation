import os
import glob
import json
import re
import cv2
import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import easyocr
from typing import Callable, Dict, Any

def setup_predictor(
    weights_path: str,
    score_thresh: float = 0.5,
    device: torch.device = None
) -> Callable[[Any], Dict]:
    """
    Loads a Faster R-CNN model fine-tuned for 2 checkbox classes.
    Returns a predictor(image_array) -> {boxes, scores, labels}.
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # load base model
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    in_feats = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_feats, num_classes=3)
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.to(device).eval()

    def predictor(img_array):
        # img_array: BGR or grayscale
        if img_array.ndim == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
        rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        tensor = torchvision.transforms.functional.to_tensor(rgb).to(device)
        with torch.no_grad():
            out = model([tensor])[0]
        return out

    predictor.score_thresh = score_thresh
    return predictor

def update_checkbox_json(
    json_path: str,
    segmented_root: str,
    predictor: Callable[[Any], Dict],
    output_json: str = "../Output/JSON/ExtractedText.json"
) -> Dict[str, bool]:
    """
    Finds all Checkbox*.jpg under segmented_root,
    inverts each patch, runs predictor, reads text via OCR,
    and writes results back under a "Checkbox" key in the master JSON.
    """
    reader = easyocr.Reader(['en'])
    pattern = os.path.join(segmented_root, "*", "SegmentedPatches", "Checkbox*.jpg")
    imgs = glob.glob(pattern, recursive=True)
    if not imgs:
        print("[!] No checkbox images found.")
        return {}

    # load or init JSON
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    results: Dict[str,bool] = {}
    for path in imgs:
        fname = os.path.splitext(os.path.basename(path))[0]
        base = re.sub(r'_\d+$', '', fname)

        gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        inv = cv2.bitwise_not(gray)

        pred = predictor(inv)
        boxes = pred['boxes'].cpu().numpy()
        scores = pred['scores'].cpu().numpy()
        labels = pred['labels'].cpu().numpy()

        # choose highest-confidence detection above threshold
        checked = False
        for b, s, l in zip(boxes, scores, labels):
            if s < predictor.score_thresh:
                continue
            checked = (l == 1)  # 1→checked, 2→unchecked
            break

        # get text nearby
        txts = reader.readtext(inv, detail=0)
        key = " ".join(txts).strip() or base
        results[key] = checked

    data["Checkbox"] = results
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"[✓] Checkbox results merged into {output_json}")
    return results
