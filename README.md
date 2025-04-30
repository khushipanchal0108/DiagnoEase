# DiagnoEase – AI-Powered Blood Report Summarization & Health Insight System

## 🩺 Project Overview

**DiagnoEase** is an AI-powered mobile application that transforms complex medical blood test reports (CBC) into clear, layman-friendly summaries. Using deep learning and NLP, it helps users understand their health without needing medical expertise.

This system removes the need for frequent clinical consultations by offering instant AI interpretations of blood reports, empowering users to take control of their health — anytime, anywhere.



## 🚀 Why This Matters

Millions of patients receive CBC reports each year but struggle to understand the technical jargon. DiagnoEase:

- Extracts data from PDF reports automatically
- Summarizes results in human-readable language
- Delivers insights directly to users' smartphones

This makes healthcare more accessible, especially in underserved areas, and reduces unnecessary hospital visits for basic explanations.



## 📊 Dataset

- ~10,000 anonymized CBC entries from students + public sources (Kaggle, Mendeley)
- Extracted parameters include:
  - Hemoglobin, RBC, WBC, Platelets
  - PCV, MCV, MCH, MCHC, RDW, MPV
  - Differential leukocyte counts, PCT, PDW
- Each report is paired with a custom-written summary indicating possible health conditions.
- Stored in structured Excel sheets for training and testing.



## ⚙️ Methodology

- **Data Collection**: Gathered CBC reports (PDFs + spreadsheets)
- **Preprocessing**: Extracted values using `pdfplumber`; cleaned and tokenized summaries
- **Model Training**: Fine-tuned T5 and BART models on report-summary pairs
- **Evaluation**: Used ROUGE scores to measure summary quality
- **Deployment**:
  - Python Flask backend for inference
  - Kotlin Android frontend for user interaction



## 📱 Android App Details

The DiagnoEase Android app is the main interface for users. It allows them to upload reports and receive instant feedback.

### Core Features:

- 📄 **PDF Upload**: Users can select blood report PDFs directly from their phone
- 🌐 **Flask API Integration**: Uses Retrofit to connect with the backend
- 🧠 **AI Summary**: Receives a health summary in simple terms via API response
- 🖥️ **User Interface**: Clean, modern UI using Android Material Design components
- ☁️ **Internet Connectivity**: Works with both local Flask (via ngrok) and hosted APIs

### Android Stack:

- **Language**: Kotlin
- **Architecture**: MVVM
- **Libraries**: Retrofit, Coroutines, GSON/Moshi, AndroidX
- **Build Tool**: Gradle
- **IDE**: Android Studio



## 💡 Tech Stack

| Component | Tools Used |
|----------|-------------|
| Frontend | Kotlin (Android App) |
| Backend | Python + Flask |
| AI Model | HuggingFace Transformers (T5, BART) |
| PDF Processing | PyMuPDF, pdfplumber |
| NLP Preprocessing | NLTK, Scikit-learn |
| Evaluation | ROUGE metrics (`evaluate` library) |
| API Tunneling | Ngrok |



## 📱 How It Works

1. **Upload**: User selects a PDF CBC report in the Android app.
2. **Request**: The app sends it to the Flask backend using Retrofit.
3. **Processing**:
   - Values are extracted from the report
   - A T5 model generates a health summary
4. **Response**: The summary is returned and shown in the app.



## 🌐 Real-World Impact

- Makes lab reports understandable for all
- Reduces confusion, fear, and reliance on medical professionals for basic interpretation
- Empowers users to make timely health decisions
- Increases access to healthcare insights in rural/remote areas



## 🔭 Future Scope

- Expand to other diagnostic reports beyond CBC
- Add user history, trends, and visualizations
- Integrate nutrition/diet suggestions
- Deploy on Google Play Store with account login
- Implement data privacy, encryption, and secure cloud storage




## 🌐 Hosting Flask Backend Online using Ngrok

To allow the Android app to communicate with your locally running Flask API, we use **Ngrok** to expose the `localhost:5000` server to the internet through a public URL.

### ✅ Step-by-Step Setup

#### 1. **Activate Python Virtual Environment**
Make sure your environment is activated before running the app:

```bash
venv\Scripts\activate
```

#### 2. **Start the Flask App**
Run the backend server:

```bash
python app.py
```

This will start your app on:  
`http://127.0.0.1:5000/`

> ⚠️ Keep this terminal open — it needs to stay running.

#### 3. **Install and Authenticate Ngrok**
If you're using Ngrok for the first time on a new machine, get your **AuthToken** from [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken) and run:

```bash
ngrok config add-authtoken <YOUR_AUTHTOKEN>
```

Example:

```bash
ngrok config add-authtoken 2ofLNa8LyGvp6uEll7ZBvfqT15j_66vu12VsX92Uofsa89hWM
```

#### 4. **Start Ngrok to Tunnel Port 5000**
You can either use a dynamic random domain:

```bash
ngrok http 5000
```

Or, if you have reserved a **custom subdomain** (e.g., `reliably-vocal-meerkat.ngrok-free.app`):

```bash
ngrok http --domain=reliably-vocal-meerkat.ngrok-free.app 5000
```

Ngrok will now generate a public URL like:  
`https://reliably-vocal-meerkat.ngrok-free.app`  
which forwards to your local server on port 5000.

#### 5. **Use This URL in the Android App**
In your Android project (usually within the Retrofit client setup), make sure to use the Ngrok-generated URL as your **base URL** so the app can send requests to the Flask server.



## 🙌 Get Involved

We're always looking for collaborators — developers, healthcare professionals, designers, or anyone interested in democratizing healthcare!

📧 **jheelturakhia@gmail.com**  
📧 **panchalk2004@gmail.com**
