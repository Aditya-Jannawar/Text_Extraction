from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import pytesseract
import fitz  # PyMuPDF
import os
from docx import Document
from fpdf import FPDF
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['EXPORT_FOLDER'] = './exports'

# Create the folder if it does not exist
if not os.path.exists(app.config['EXPORT_FOLDER']):
    os.makedirs(app.config['EXPORT_FOLDER'])

# Ensure upload and export folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

def convert_pdf_to_images(pdf_path):
    """Convert each page of a PDF to an image."""
    images = []
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"page_{page_num}.png")
        pix.save(image_path)
        images.append(image_path)
    return images

def extract_text_from_image(image_path):
   text = pytesseract.image_to_string(image_path)
   errors = []

    # Check for common OCR issues in extracted text
   if '' in text or '•' in text or '*' in text or '+' in text:

        errors.append("Unrecognized symbols (e.g., bullets) found, which OCR could not interpret correctly.")

   if not text.strip():
        errors.append("No text extracted. The image may be too blurry or contain non-standard characters.")

    # Add more checks for specific patterns you want to handle
   if re.search(r'\b(?:\d{2,4}-\d{2,4})\b', text) is None:
        errors.append("Expected date or serial patterns not found, possibly due to formatting issues. ")

   return text, errors

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload, convert PDF to images if needed, and extract text."""
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file uploaded"}), 400
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # If PDF, convert to images
        if filename.lower().endswith('.pdf'):
            images = convert_pdf_to_images(file_path)
        else:
            images = [file_path]

    # Extract text from each image and capture status
        extracted_text = ""
        extraction_errors = []  # Collect errors in a separate list


        for i, image in enumerate(images):
            text, errors = extract_text_from_image(image)
            if "errors":
                extraction_errors.append(f"Page {i + 1}: {errors}")  # Add error detail
            else:
                extracted_text += f"--- Page {i + 1} ---\n{text}\n"

        # Clean up image files after extraction
            if image != file_path and os.path.exists(image):
                os.remove(image)

    # Clean up extra line spacing in extracted text
        cleaned_text =re.sub(r'\n+', ' ', extracted_text.strip()) # Remove extra line breaks

    # Include cleaned text and error list in response
        return jsonify({"text": cleaned_text, "errors": extraction_errors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test-tesseract', methods=['GET'])
def test_tesseract():
    try:
        output = pytesseract.image_to_string('uploads/google_img.png')  # Provide a valid path
        return jsonify({"message": "Tesseract working", "output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/export', methods=['POST'])
def export_text():
    data = request.json
    text = data.get("text")
    export_type = data.get("type")

    # Replace unsupported characters
    text = text.encode('ascii', 'ignore').decode('ascii')

    if export_type == "pdf":
        pdf_path = os.path.join(app.config['EXPORT_FOLDER'], "exported_text.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=0)
        pdf.set_font("Helvetica", size=12)
        
        lines = text.splitlines()
        for line in lines:
            pdf.multi_cell(0, 10, line)
            pdf.ln()
        pdf.output(pdf_path)
        return jsonify({"path": f"/download/exported_text.pdf"})

    elif export_type == "word":
        doc_path = os.path.join(app.config['EXPORT_FOLDER'], "exported_text.docx")
        doc = Document()
        doc.add_paragraph(text)
        doc.save(doc_path)
        return jsonify({"path": f"/download/exported_text.docx"})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['EXPORT_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
