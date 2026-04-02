import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# import your existing pipeline entrypoint; adjust the path as needed
import sys, os

# add the parent directory (MainCode/) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Main import main_pipeline as ai_main

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "annotated"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # allow React dev server

@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # save incoming PDF
    in_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(in_path)

    # call your AI pipeline
    # assume ai_main returns a dict with keys "json" and "pdf_path"
    result = ai_main(in_path, OUTPUT_FOLDER)  
    # e.g. result = {"json": {...}, "pdf_path": "annotated/11800_validated.pdf"}

    # expose the processed PDF via Flask
    pdf_relpath = os.path.basename(result["pdf_path"])
    return jsonify({
        "data": result["json"],
        "pdfUrl": f"http://localhost:5001/annotated/{pdf_relpath}"
    })

@app.route("/annotated/<path:filename>")
def annotated_pdf(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, mimetype="application/pdf")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
