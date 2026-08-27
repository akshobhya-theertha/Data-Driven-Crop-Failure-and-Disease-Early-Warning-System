# Data-Driven Crop Failure and Disease Early Warning System

AI-based tomato leaf disease detection using Python, TensorFlow, Keras, and Flask.

## Requirements

- Python 3.8+
- Kaggle API credentials (`kaggle.json` in `~/.kaggle/` or `C:\Users\<user>\.kaggle\`)

## Setup

```bash
pip install -r requirements.txt
```

Place your `kaggle.json` (from Kaggle Account → Create New API Token) in:
- **Windows:** `C:\Users\<YourUsername>\.kaggle\kaggle.json`
- **Linux/Mac:** `~/.kaggle/kaggle.json`

## Usage

### Option A: Full training (requires Kaggle dataset)

1. **Accept dataset terms** on Kaggle (fixes 403 error):
   - Go to https://www.kaggle.com/datasets/samanfatima7/tomato-leaf-disease
   - Click "Download" or "New Notebook" to accept terms

2. **Train the model**:
   ```bash
   python train_model.py
   ```

### Option B: Demo model (no dataset needed)

If Kaggle gives 403 or you want to test the UI first:

```bash
python create_demo_model.py
```

### Run the Flask app

```bash
python app.py
```

Open browser: **http://127.0.0.1:5000**

## API

**POST /predict**
- Body: `multipart/form-data` with `file` (image)
- Returns: JSON with `crop_name`, `disease_name`, `confidence`, `remedies`, `soil_recommendation`, `environment_recommendation`

## Project Structure

```
project/
├── dataset/              # Loaded via Kaggle API
├── model/
│   ├── crop_disease_model.h5
│   └── class_names.json
├── static/css/
├── templates/
│   └── index.html
├── app.py
├── train_model.py
├── kaggle_loader.py
├── disease_remedies.py
├── requirements.txt
└── README.md
```
