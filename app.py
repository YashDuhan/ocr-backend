from flask import Flask, request, jsonify
import os
from paddleocr import PaddleOCR
from werkzeug.utils import secure_filename

# Initialize PaddleOCR with English language support
ocr = PaddleOCR(use_angle_cls=True, lang='en')

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/extract-text", methods=["POST"])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Run OCR on the image
    result = ocr.ocr(filepath, cls=True)
    
    # Extract text
    extracted_text = []
    for line in result:
        for box in line:
            extracted_text.append(box[1][0])
    
    return jsonify({"text": " ".join(extracted_text)})

if __name__ == "__main__":
    app.run(debug=True)
