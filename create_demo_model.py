"""
Create a runnable multi-crop demo model (Tomato + Potato + Bell Pepper).
Use this so the Flask web app can start quickly.
For real accuracy, later run: python train_model.py
"""
import json
from pathlib import Path

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "model"
IMG_SIZE = 224

# Must match dataset folder names under dataset/tomato/train
CLASS_NAMES = [
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


def main():
    MODEL_DIR.mkdir(exist_ok=True)

    base = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base.trainable = False
    x = base.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    out = Dense(len(CLASS_NAMES), activation="softmax")(x)
    model = Model(inputs=base.input, outputs=out)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    model_path = MODEL_DIR / "crop_disease_model.h5"
    model.save(model_path)

    with open(MODEL_DIR / "class_names.json", "w", encoding="utf-8") as f:
        json.dump(CLASS_NAMES, f, indent=2)

    print(f"Demo model saved to {model_path}")
    print(f"Classes ({len(CLASS_NAMES)}):")
    for name in CLASS_NAMES:
        print(f"  - {name}")
    print("Run the web app with: python run_webapp.py")
    print("NOTE: Placeholder weights. Run 'python train_model.py' for real predictions.")


if __name__ == "__main__":
    main()
