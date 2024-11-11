import os
import re
import torch
from flask import Flask, request, render_template, redirect, url_for, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pdfplumber
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set an upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("t5-small")  # Load base model
model.load_state_dict(torch.load("C:\\Users\\Khushi Panchal\\Desktop\\PROJECT\\pdf_summary_api\\modelnew.pt", map_location=torch.device('cpu')))
model.eval()  # Put the model in evaluation mode

tokenizer = T5Tokenizer.from_pretrained("t5-small")  # Adjust to your finetuned model path

# List of parameters to extract from the PDF
parameters_list = [
    "HAEMOGLOBIN (HB) :", "RED BLOOD CELL (RBC) COUNT :", "PCV (PACKED CELL VOLUME) :",
    "MCV (MEAN CORPUSCULAR VOLUME) :", "MCH (MEAN CORPUSCULAR HEMOGLOBIN) :",
    "MCHC (MEAN CORPUSCULAR HB.CONC.) :", "RED CELL DISTRIBUTION WIDTH-CV (RDW-CV) :",
    "TOTAL LEUCOCYTE (WBC) COUNT : ", "NEUTROPHIL :", "LYMPHOCYTES :",
    "PLATELET COUNT :", "MEAN PLATELET VOLUME ( MPV ) : "
]

# Route to display the upload form
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle PDF upload
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Redirect to the summary page
        return redirect(url_for('process_pdf', filename=file.filename))

    return jsonify({'error': 'Invalid file type, only PDFs are allowed'}), 400

# Route to process the uploaded PDF and generate the summary
@app.route('/process/<filename>')
def process_pdf(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Extract text from the uploaded PDF file
    text = extract_text_from_pdf(file_path)

    # Extract medical values from text
    medical_values, gender = extract_medical_values(text)

    # Generate the summary using the model
    summary = generate_summary(medical_values)

    return render_template('summary.html', summary=summary, extracted_data=medical_values)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to extract medical values from the text
def extract_medical_values(extracted_text):
    gender_match = re.search(r'AGE/SEX\s*:\s*\d+\s*[Yy]/([MFmf])', extracted_text)
    gender = gender_match.group(1).upper() if gender_match else 'Unknown'

    medical_values = {}

    for line in extracted_text.split('\n'):
        for parameter in parameters_list:
            if parameter in line:
                value_match = re.search(rf'{re.escape(parameter)}\s*([\d.]+)', line)
                value = value_match.group(1) if value_match else 'N/A'
                medical_values[parameter] = value

    return medical_values, gender

# Function to generate summary using the model
def generate_summary(input_data):
    # Only keep numeric values
    numeric_values = [value for value in input_data.values() if re.match(r'^\d+(\.\d+)?$', value)]
    
    # Join the numeric values into a string
    input_text = "Summary:\n" + ' '.join(numeric_values)

    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        summary_ids = model.generate(inputs['input_ids'], max_length=150, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

if __name__ == '_main_':
    app.run(debug=True)
