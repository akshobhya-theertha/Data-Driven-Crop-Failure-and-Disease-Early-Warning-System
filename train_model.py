"""
Crop Leaf Disease Detection - Model Training Script
Trains Tomato + Potato + Bell Pepper from dataset/tomato/train and dataset/tomato/val.
"""
import os
import json
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.utils import Sequence

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)

# Constants
IMG_SIZE = 224
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "32"))
EPOCHS = int(os.environ.get("EPOCHS", "8"))
LEARNING_RATE = 1e-4
FINE_TUNE_EPOCHS = int(os.environ.get("FINE_TUNE_EPOCHS", "6"))
FINE_TUNE_AT = int(os.environ.get("FINE_TUNE_AT", "100"))
SEED = int(os.environ.get("SEED", "42"))

np.random.seed(SEED)
tf.random.set_seed(SEED)


class SafeDirectorySequence(Sequence):
    """Wrap a DirectoryIterator and skip batches that fail to load."""

    def __init__(self, base_iterator):
        super().__init__()
        self.base = base_iterator

    def __len__(self):
        return len(self.base)

    def __getitem__(self, idx):
        max_tries = max(1, len(self.base))
        attempt = 0
        current_idx = idx
        while attempt < max_tries:
            try:
                return self.base[current_idx]
            except (FileNotFoundError, OSError, UnidentifiedImageError) as e:
                print(f"[WARN] Skipping bad batch at index {current_idx}: {e}")
                current_idx = (current_idx + 1) % len(self.base)
                attempt += 1
        raise RuntimeError("Could not load any valid batch. Check dataset integrity.")

    def on_epoch_end(self):
        if hasattr(self.base, "on_epoch_end"):
            self.base.on_epoch_end()


def sanitize_iterator_files(iterator, split_name):
    """
    Remove missing/corrupted files from DirectoryIterator before training.
    This prevents crashes when OneDrive placeholders or broken files exist.
    """
    kept_filenames = []
    kept_classes = []
    skipped = 0

    for rel_path, cls_idx in zip(iterator.filenames, iterator.classes):
        full_path = Path(iterator.directory) / rel_path
        try:
            if not full_path.exists():
                skipped += 1
                continue
            with Image.open(full_path) as img:
                img.verify()
            kept_filenames.append(rel_path)
            kept_classes.append(cls_idx)
        except (FileNotFoundError, OSError, UnidentifiedImageError):
            skipped += 1

    if not kept_filenames:
        raise RuntimeError(f"No valid images found in {split_name} after sanitization.")

    iterator.filenames = kept_filenames
    iterator.samples = len(kept_filenames)
    iterator.n = len(kept_filenames)
    iterator.classes = np.array(kept_classes, dtype=np.int32)

    if hasattr(iterator, "_filepaths"):
        iterator._filepaths = [str(Path(iterator.directory) / p) for p in kept_filenames]
    if hasattr(iterator, "_set_index_array"):
        iterator._set_index_array()

    print(f"{split_name}: kept {iterator.n} images, skipped {skipped} broken/missing files.")


def get_local_dataset_dirs():
    """Return local train/val directories if present."""
    tomato_root = PROJECT_ROOT / "dataset" / "tomato"
    train_dir = tomato_root / "train"
    val_dir = tomato_root / "val"
    if train_dir.exists() and val_dir.exists():
        return train_dir, val_dir
    raise FileNotFoundError(
        f"Expected dataset at '{train_dir}' and '{val_dir}'. "
        "Please place images in those folders."
    )


def create_generators(train_dir, val_dir):
    """Create train/validation generators from directory structure."""
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=20,
        width_shift_range=0.15,
        height_shift_range=0.15,
        horizontal_flip=True,
        zoom_range=0.15,
        fill_mode="nearest",
    )
    val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

    train_gen = train_datagen.flow_from_directory(
        str(train_dir),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=True,
        seed=SEED,
    )
    val_gen = val_datagen.flow_from_directory(
        str(val_dir),
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=False,
    )
    sanitize_iterator_files(train_gen, "Train")
    sanitize_iterator_files(val_gen, "Validation")
    class_indices = dict(train_gen.class_indices)
    return SafeDirectorySequence(train_gen), SafeDirectorySequence(val_gen), class_indices


def build_model(num_classes):
    """Build MobileNetV2-based model with transfer learning."""
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
        pooling=None,
    )
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.5)(x)
    outputs = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.05),
        metrics=["accuracy"],
    )
    return model, base_model


def build_callbacks(model_path):
    """Standard callbacks for training phases."""
    return [
        EarlyStopping(
            monitor="val_accuracy",
            patience=4,
            restore_best_weights=True,
            verbose=1,
        ),
        ModelCheckpoint(
            str(model_path),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-6,
            verbose=1,
        ),
    ]


def unfreeze_for_finetuning(base_model, fine_tune_at):
    """Unfreeze top layers of base model for fine-tuning."""
    base_model.trainable = True
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False
    # Keep BatchNorm frozen for stable fine-tuning.
    for layer in base_model.layers[fine_tune_at:]:
        if isinstance(layer, BatchNormalization):
            layer.trainable = False


def train():
    """Main training pipeline."""
    print("=" * 60)
    print("Crop Leaf Disease Detection - Training (Tomato / Potato / Pepper)")
    print("=" * 60)

    print("\n[1/4] Reading local dataset folders...")
    train_dir, val_dir = get_local_dataset_dirs()
    train_gen, val_gen, class_indices = create_generators(train_dir, val_dir)

    class_names = [
        name for name, index in sorted(class_indices.items(), key=lambda item: item[1])
    ]
    print(f"Found {len(class_names)} classes")

    print("\n[2/5] Building model (MobileNetV2 + custom head)...")
    model, base_model = build_model(len(class_names))

    model_dir = PROJECT_ROOT / "model"
    model_dir.mkdir(exist_ok=True)
    model_path = model_dir / "crop_disease_model.h5"

    callbacks = build_callbacks(model_path)

    print(f"\n[3/5] Phase 1 (feature extraction) for up to {EPOCHS} epochs...")
    history_phase1 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1,
    )

    if FINE_TUNE_EPOCHS > 0:
        print(f"\n[4/5] Phase 2 (fine-tuning) for up to {FINE_TUNE_EPOCHS} epochs...")
        unfreeze_for_finetuning(base_model, FINE_TUNE_AT)
        model.compile(
            optimizer=Adam(learning_rate=1e-5),
            loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.05),
            metrics=["accuracy"],
        )
        history_phase2 = model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS + FINE_TUNE_EPOCHS,
            initial_epoch=history_phase1.epoch[-1] + 1,
            callbacks=callbacks,
            verbose=1,
        )
    else:
        history_phase2 = None

    class_map_path = model_dir / "class_names.json"
    with open(class_map_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)

    if history_phase2 and history_phase2.history.get("accuracy"):
        train_acc = history_phase2.history["accuracy"][-1]
        val_acc = history_phase2.history["val_accuracy"][-1]
    else:
        train_acc = history_phase1.history["accuracy"][-1]
        val_acc = history_phase1.history["val_accuracy"][-1]

    print("\n[5/5] Complete")
    print("=" * 60)
    print(f"Final Training Accuracy:   {train_acc * 100:.2f}%")
    print(f"Final Validation Accuracy: {val_acc * 100:.2f}%")
    print(f"Model saved to: {model_path}")
    print(f"Class names saved to: {class_map_path}")
    print("=" * 60)

    return model, class_names


if __name__ == "__main__":
    train()
