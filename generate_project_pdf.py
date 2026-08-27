"""
Generate a comprehensive project documentation PDF.
Run: python generate_project_pdf.py
Output: Project_Documentation.pdf
"""
from pathlib import Path

from fpdf import FPDF

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = PROJECT_ROOT / "Project_Documentation.pdf"


class DocPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(60, 90, 70)
        self.cell(
            0,
            8,
            "Data-Driven Crop Failure and Disease Early Warning System",
            align="C",
        )
        self.ln(4)
        self.set_draw_color(42, 122, 75)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(18, 69, 44)
        self.ln(3)
        self.multi_cell(0, 8, title)
        self.set_draw_color(196, 163, 90)
        y = self.get_y()
        self.line(15, y, 80, y)
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(42, 122, 75)
        self.ln(2)
        self.multi_cell(0, 7, title)
        self.ln(1)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 40, 35)
        self.multi_cell(0, 5.5, text)
        self.ln(1.5)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 40, 35)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.5, f"- {text}")
        self.ln(0.5)

    def code_block(self, text):
        self.set_fill_color(232, 243, 236)
        self.set_font("Courier", "", 8.5)
        self.set_text_color(20, 50, 35)
        self.multi_cell(0, 4.8, text, fill=True)
        self.ln(2)


def build_pdf():
    pdf = DocPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # Cover
    pdf.ln(25)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(18, 69, 44)
    pdf.multi_cell(0, 10, "Data-Driven Crop Failure and\nDisease Early Warning System", align="C")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(80, 100, 85)
    pdf.multi_cell(0, 7, "Complete Project Documentation", align="C")
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 10)
    pdf.multi_cell(
        0,
        6,
        "Features, Algorithms, Libraries, Models, Architecture & Commands",
        align="C",
    )
    pdf.ln(10)
    pdf.set_draw_color(42, 122, 75)
    pdf.line(55, pdf.get_y(), 155, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 50, 45)
    pdf.multi_cell(
        0,
        6,
        "This document explains every major component used in the project: "
        "web interface, disease detection logic, deep learning model, remedies "
        "(English + Kannada), text-to-speech, libraries, algorithms, and the "
        "exact commands needed to install dependencies and run the application.",
        align="C",
    )

    # 1. Overview
    pdf.add_page()
    pdf.section_title("1. Project Overview")
    pdf.body(
        "This project is an AI-assisted crop leaf disease early warning web application. "
        "A farmer or user uploads a leaf image. The system detects the crop and disease, "
        "shows a confidence score, and provides treatment remedies in English and Kannada. "
        "Users can listen to remedies using Text-to-Speech buttons (Listen / Kannada Listen)."
    )
    pdf.sub_title("Supported Crops")
    pdf.bullet("Tomato")
    pdf.bullet("Potato")
    pdf.bullet("Bell Pepper (Capsicum)")
    pdf.sub_title("Supported Disease Classes (15 total)")
    classes = [
        "Pepper,_bell___Bacterial_spot",
        "Pepper,_bell___healthy",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Potato___healthy",
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___Leaf_Mold",
        "Tomato___Septoria_leaf_spot",
        "Tomato___Spider_mites Two-spotted_spider_mite",
        "Tomato___Target_Spot",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Tomato_mosaic_virus",
        "Tomato___healthy",
    ]
    for c in classes:
        pdf.bullet(c)

    # 2. Features
    pdf.section_title("2. Features Explained")
    features = [
        (
            "Two-screen Web UI",
            "Screen 1 is for uploading a leaf image. Screen 2 shows analysis results "
            "after Detect/Analyze is pressed. Users can return with Upload another.",
        ),
        (
            "Image Upload & Preview",
            "Accepts JPG, JPEG, PNG, and WEBP. Shows an on-page preview before analysis.",
        ),
        (
            "Filename-first Disease Detection (Scenario 1)",
            "Primary detection method. Matches the uploaded file name to dataset image names, "
            "class folder names inside the filename, keyword markers, or PlantVillage-style "
            "codes (for example RS_LB, Early.B, JR_B.Spot).",
        ),
        (
            "Model Fallback Detection (Scenario 2)",
            "If filename matching fails, the MobileNetV2-based deep learning model predicts "
            "the disease class from the image pixels.",
        ),
        (
            "Crop & Disease Names (English + Kannada)",
            "Results show crop and disease names in English and Kannada.",
        ),
        (
            "Confidence Score",
            "Displayed in an approximate 85% to 95% range for a stable user-facing score.",
        ),
        (
            "Severity Level",
            "Maps each disease to severity such as None, Medium, High, or Very High.",
        ),
        (
            "Remedies (English + Kannada)",
            "Practical treatment text is shown in both languages for every supported disease.",
        ),
        (
            "Soil & Environment Guidance",
            "Additional recommendations for soil conditions and growing environment.",
        ),
        (
            "English Text-to-Speech (Listen)",
            "Browser Web Speech API reads English remedies aloud.",
        ),
        (
            "Kannada Text-to-Speech (Listen button in Kannada)",
            "Speaks Kannada remedies. Uses a local Kannada voice if installed; otherwise "
            "uses the server endpoint /tts/kn which generates Kannada audio.",
        ),
        (
            "Modern Agricultural UI",
            "Green-sage-gold themed interface with responsive layout for desktop and mobile.",
        ),
    ]
    for title, desc in features:
        pdf.sub_title(title)
        pdf.body(desc)

    # 3. Architecture / Files
    pdf.add_page()
    pdf.section_title("3. Project Structure & Important Files")
    files = [
        ("run_webapp.py", "Main entry file to launch the web application."),
        ("app.py", "Flask backend: upload, predict, filename matching, TTS endpoint, API."),
        ("disease_remedies.py", "English/Kannada remedies, severity, disease & crop name maps."),
        ("train_model.py", "Trains MobileNetV2 transfer-learning model on local dataset."),
        ("create_demo_model.py", "Creates a quick placeholder model so the app can start."),
        ("kaggle_loader.py", "Optional helper to download datasets via Kaggle API."),
        ("requirements.txt", "Python package dependency list."),
        ("run.ps1", "Windows helper script to install deps and start the app."),
        ("templates/index.html", "Frontend pages, upload/analysis UI, TTS buttons."),
        ("static/css/style.css", "Visual styling and color theme."),
        ("model/crop_disease_model.h5", "Saved Keras/TensorFlow model weights."),
        ("model/class_names.json", "Ordered list of class labels used by the model."),
        ("dataset/tomato/train & val", "Training/validation images by class folders."),
        ("uploads/", "Temporary folder for uploaded images."),
    ]
    for name, desc in files:
        pdf.bullet(f"{name}: {desc}")

    # 4. Algorithms
    pdf.section_title("4. Algorithms & Techniques Used")
    pdf.sub_title("4.1 Transfer Learning (MobileNetV2)")
    pdf.body(
        "A pretrained MobileNetV2 network (ImageNet weights) is used as a feature extractor. "
        "A custom classification head is added for the 15 crop-disease classes. "
        "This reduces training time and improves accuracy with limited agricultural data."
    )
    pdf.sub_title("4.2 Convolutional Neural Network (CNN) Concept")
    pdf.body(
        "MobileNetV2 is a CNN architecture. Convolution layers extract visual patterns "
        "(spots, blight lesions, leaf texture). Global Average Pooling compresses features, "
        "then Dense layers produce class probabilities via Softmax."
    )
    pdf.sub_title("4.3 Softmax Classification")
    pdf.body(
        "The final layer uses Softmax to convert scores into probabilities across all classes. "
        "The class with the highest probability (argmax) is selected as the prediction."
    )
    pdf.sub_title("4.4 Test-Time Augmentation (TTA)")
    pdf.body(
        "At prediction time the app averages results from the original image and a "
        "horizontally flipped version to make predictions more stable."
    )
    pdf.sub_title("4.5 Image Preprocessing")
    pdf.body(
        "Images are resized to 224x224 RGB and preprocessed with MobileNetV2 preprocessing "
        "(scaling/normalization expected by the pretrained network)."
    )
    pdf.sub_title("4.6 Data Augmentation (Training)")
    pdf.body(
        "During training, rotations, shifts, zoom, and horizontal flips are applied so the "
        "model generalizes better to real field photos."
    )
    pdf.sub_title("4.7 Fine-Tuning")
    pdf.body(
        "After initial training with a frozen base, upper MobileNetV2 layers can be unfrozen "
        "and trained at a lower learning rate for better domain adaptation."
    )
    pdf.sub_title("4.8 Filename Matching Heuristics")
    pdf.body(
        "Exact/normalized filename index lookup against the dataset; class-name substring "
        "matching; crop+disease keyword rules; PlantVillage code pattern matching with "
        "regular expressions."
    )
    pdf.sub_title("4.9 Confidence Display Mapping")
    pdf.body(
        "Raw model probability is mapped into an approximate 85-95% display range with light "
        "deterministic jitter based on filename hashing for natural-looking scores."
    )
    pdf.sub_title("4.10 Training Callbacks")
    pdf.body(
        "EarlyStopping, ModelCheckpoint, and ReduceLROnPlateau are used during training to "
        "avoid overfitting, save the best model, and adapt learning rate."
    )

    # 5. Model
    pdf.add_page()
    pdf.section_title("5. Deep Learning Model Details")
    pdf.bullet("Base model: MobileNetV2 (TensorFlow/Keras Applications)")
    pdf.bullet("Input size: 224 x 224 x 3")
    pdf.bullet("Pretrained weights: ImageNet")
    pdf.bullet("Head: GlobalAveragePooling2D + BatchNormalization + Dense(256, ReLU) + Dropout(0.5) + Dense(num_classes, Softmax)")
    pdf.bullet("Loss: Categorical Crossentropy (label smoothing during training)")
    pdf.bullet("Optimizer: Adam")
    pdf.bullet("Saved format: crop_disease_model.h5")
    pdf.bullet("Labels file: class_names.json")
    pdf.body(
        "create_demo_model.py builds a runnable placeholder model quickly. "
        "For real accuracy, run train_model.py on the local train/val folders."
    )

    # 6. Libraries
    pdf.section_title("6. Libraries & Packages Used")
    libs = [
        ("Flask", "Web framework serving HTML pages and REST API endpoints."),
        ("Werkzeug", "Utilities used by Flask (secure_filename, request handling)."),
        ("Waitress", "Production-style WSGI server for more reliable Windows serving."),
        ("TensorFlow / Keras", "Deep learning framework for model build, train, and predict."),
        ("NumPy", "Array operations for image batches and prediction vectors."),
        ("Pillow (PIL)", "Image loading, RGB conversion, resize, flip for TTA."),
        ("scikit-learn", "Machine learning utilities available for dataset/training workflows."),
        ("Kaggle API (optional)", "Programmatic dataset download if configured."),
        ("Jinja2 (via Flask)", "HTML template rendering for index.html."),
        ("Browser Web Speech API", "Client-side English speech synthesis."),
        ("urllib (Python stdlib)", "Fetches Kannada TTS audio for /tts/kn endpoint."),
        ("hashlib / re / json / pathlib", "Hashing, regex filename rules, config, file paths."),
    ]
    for name, desc in libs:
        pdf.bullet(f"{name}: {desc}")

    pdf.sub_title("Frontend Technologies")
    pdf.bullet("HTML5 for structure and dual-screen interface")
    pdf.bullet("CSS3 for agricultural green/gold theme, responsive layout, animations")
    pdf.bullet("JavaScript (Fetch API) for image upload and /predict calls")
    pdf.bullet("Google Fonts: Fraunces, Outfit, Noto Sans Kannada")

    # 7. API
    pdf.section_title("7. Backend API Endpoints")
    pdf.sub_title("GET /")
    pdf.body("Serves the main web application UI.")
    pdf.sub_title("POST /predict")
    pdf.body(
        "Accepts multipart form field file (or image). Returns JSON including crop_name, "
        "crop_name_kn, disease_name, disease_name_kn, severity, confidence, remedies, "
        "remedies_kn, soil_recommendation, environment_recommendation, detection_source."
    )
    pdf.sub_title("GET /tts/kn?q=TEXT")
    pdf.body("Returns MPEG audio for Kannada text used by the Kannada Listen button.")

    # 8. Detection flow
    pdf.section_title("8. End-to-End Detection Flow")
    pdf.bullet("1. User selects a leaf image on Upload screen.")
    pdf.bullet("2. User clicks Analyze image; UI switches to Analysis screen.")
    pdf.bullet("3. Backend saves upload and tries Scenario 1 filename detection.")
    pdf.bullet("4. If no filename match, Scenario 2 runs MobileNetV2 prediction with TTA.")
    pdf.bullet("5. Backend attaches remedies, Kannada names, severity, confidence.")
    pdf.bullet("6. Frontend shows bilingual results and enables Listen buttons.")

    # 9. Commands
    pdf.add_page()
    pdf.section_title("9. Commands to Install Everything")
    pdf.body(
        "Open PowerShell and run the following from the project folder "
        "(DDCF\\DDCF). These commands create a virtual environment and install "
        "all required packages and dependencies from requirements.txt."
    )
    pdf.sub_title("Windows (PowerShell) - Full Install")
    pdf.code_block(
        "cd \"c:\\Users\\shrey\\OneDrive\\Desktop\\DDCF\\DDCF\"\n"
        "py -3 -m venv .venv\n"
        ".\\.venv\\Scripts\\Activate.ps1\n"
        "python -m pip install --upgrade pip\n"
        "pip install -r requirements.txt"
    )
    pdf.sub_title("One-line package install (after venv is activated)")
    pdf.code_block("pip install -r requirements.txt")
    pdf.sub_title("Packages installed by requirements.txt")
    pdf.bullet("flask, Werkzeug, waitress")
    pdf.bullet("tensorflow")
    pdf.bullet("numpy, Pillow, scikit-learn")
    pdf.bullet("kaggle (optional dataset download)")
    pdf.body(
        "TensorFlow also pulls related dependencies such as keras, h5py, grpcio, "
        "protobuf, and others automatically."
    )

    pdf.section_title("10. Commands to Run the Project")
    pdf.sub_title("A) Create / refresh a runnable model (first time)")
    pdf.code_block(
        "cd \"c:\\Users\\shrey\\OneDrive\\Desktop\\DDCF\\DDCF\"\n"
        ".\\.venv\\Scripts\\Activate.ps1\n"
        "python create_demo_model.py"
    )
    pdf.sub_title("B) Start the Web App (main command)")
    pdf.code_block(
        "cd \"c:\\Users\\shrey\\OneDrive\\Desktop\\DDCF\\DDCF\"\n"
        ".\\.venv\\Scripts\\Activate.ps1\n"
        "python run_webapp.py"
    )
    pdf.body(
        "Then open a browser at: http://127.0.0.1:5000\n"
        "The file used to run the web app is: run_webapp.py"
    )
    pdf.sub_title("C) Alternative launchers")
    pdf.code_block("python app.py")
    pdf.code_block(".\\run.ps1")
    pdf.sub_title("D) Train a real model on your dataset (optional, slower)")
    pdf.code_block(
        "cd \"c:\\Users\\shrey\\OneDrive\\Desktop\\DDCF\\DDCF\"\n"
        ".\\.venv\\Scripts\\Activate.ps1\n"
        "python train_model.py"
    )

    # 11. How to use app
    pdf.section_title("11. How to Use the Web Application")
    pdf.bullet("1. Start the server with python run_webapp.py")
    pdf.bullet("2. Open http://127.0.0.1:5000")
    pdf.bullet("3. Choose a leaf image (preferably original dataset filename for best match)")
    pdf.bullet("4. Click Analyze image")
    pdf.bullet("5. View English + Kannada disease names, confidence, remedies, soil, environment")
    pdf.bullet("6. Click Listen for English speech, or the Kannada Listen button for Kannada speech")
    pdf.bullet("7. Click Upload another to analyze a new image")

    # 12. Notes
    pdf.section_title("12. Important Notes")
    pdf.bullet(
        "Filename-first detection is enabled by default because it is accurate when "
        "uploading images that already exist in the dataset."
    )
    pdf.bullet(
        "The demo model lets the UI run immediately; train_model.py is needed for strong "
        "image-only predictions on unseen photos."
    )
    pdf.bullet(
        "Kannada speech works best with internet access for the /tts/kn audio service, "
        "or with a Kannada system voice pack installed."
    )
    pdf.bullet("Recommended Python: 3.9 to 3.13 with a matching TensorFlow wheel.")

    pdf.ln(6)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(18, 69, 44)
    pdf.multi_cell(0, 7, "End of Documentation", align="C")
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(
        0,
        5,
        "Generated for the DDCF Crop Disease Early Warning System project.",
        align="C",
    )

    pdf.output(str(OUTPUT_PATH))
    return OUTPUT_PATH


if __name__ == "__main__":
    path = build_pdf()
    print(f"PDF created: {path}")
