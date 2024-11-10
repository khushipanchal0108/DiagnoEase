
```markdown
# PDF Summary API


project_folder/
│
├── app.py                  # Flask app
└── t5_finetuned_model.pt    # Your fine-tuned T5 model

## Setup Instructions
```
### 1. Go to your desired location (Desktop, Documents, etc.)
```bash
cd path/to/your/desired/location
```

### 2. Navigate into the folder
```bash
cd pdf_summary_api
```

### 3. Create a virtual environment
```bash
python3 -m venv venv
```

### 4. Activate the virtual environment

**For Windows:**
```bash
venv\Scripts\activate
```

**For Mac/Linux:**
```bash
source venv/bin/activate
```

### 5. Install the required dependencies
```bash
pip install flask torch transformers pdfplumber sentencepiece
```

### 6. If Execution Policy Issue occurs
If you encounter an **Execution Policy Issue**, run the following command:
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then, activate the virtual environment again:
```bash
venv\Scripts\activate
```

### 7. To run the app
```bash
flask run
```

The Flask app will run locally, and you can access it at `http://127.0.0.1:5000/`.

## License
MIT License
```

This version is short, to the point, and includes all the necessary steps without extra explanation. Let me know if you need further changes!


