"""
Kaggle API Dataset Loader for Tomato Leaf Disease Dataset
Fetches dataset programmatically - NO manual download required
"""
import os
import zipfile
from pathlib import Path


def get_project_root():
    """Get the project root directory dynamically."""
    return Path(__file__).resolve().parent


def get_dataset_path():
    """Get the dataset directory path."""
    return get_project_root() / "dataset"


def load_dataset():
    """
    Download and extract the tomato leaf disease dataset from Kaggle using API.
    Dataset: samanfatima7/tomato-leaf-disease
    """
    dataset_path = get_dataset_path()
    dataset_path.mkdir(parents=True, exist_ok=True)
    
    zip_path = dataset_path / "tomato-leaf-disease.zip"
    
    # Check if already extracted (any folder with images)
    for sub in dataset_path.iterdir():
        if sub.is_dir():
            imgs = list(sub.rglob("*.jpg")) + list(sub.rglob("*.png"))
            if len(imgs) >= 10:
                return str(dataset_path)
    
    # Try datasets in order - some may require accepting terms on Kaggle first
    datasets_to_try = [
        "samanfatima7/tomato-leaf-disease",
        "kaustubhb999/tomatoleaf",
        "noulam/tomato",  # PlantVillage tomato
    ]
    
    last_error = None
    for dataset_id in datasets_to_try:
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            print(f"Trying dataset: {dataset_id}")
            api.dataset_download_files(
                dataset_id,
                path=str(dataset_path),
                unzip=True
            )
            last_error = None
            break
        except Exception as e:
            last_error = e
            print(f"  Failed: {e}")
            continue
    
    if last_error is not None:
        # If API fails, try to extract existing zip (any .zip in dataset folder)
        zips = list(dataset_path.glob("*.zip"))
        if zips:
            print("Extracting existing zip...")
            with zipfile.ZipFile(zips[0], 'r') as zip_ref:
                zip_ref.extractall(dataset_path)
            zips[0].unlink(missing_ok=True)
        else:
            raise RuntimeError(
                "Could not download any dataset. Ensure:\n"
                "1. Kaggle API is installed: pip install kaggle\n"
                "2. kaggle.json is in C:\\Users\\<user>\\.kaggle\\ (Windows) or ~/.kaggle/ (Linux/Mac)\n"
                "3. kaggle.json has valid username and key\n"
                "4. Accept dataset terms: visit https://www.kaggle.com/datasets/samanfatima7/tomato-leaf-disease and click 'Download'\n"
                f"Last error: {last_error}"
            )
    
    return str(dataset_path)


def find_image_directories(base_path):
    """
    Find class directories containing images.
    Handles various dataset structures (nested folders, different naming).
    """
    base = Path(base_path)
    class_dirs = []
    
    # Common tomato disease class folder patterns
    patterns = [
        "*healthy*", "*Healthy*",
        "*bacterial*", "*Bacterial*",
        "*blight*", "*Blight*",
        "*mold*", "*Mold*",
        "*septoria*", "*Septoria*",
        "*spider*", "*Spider*",
        "*mosaic*", "*Mosaic*",
        "*target*", "*Target*",
        "*curl*", "*Curl*",
        "*spot*", "*Spot*",
        "*leaf*", "*Leaf*",
    ]
    
    # Search for directories with images
    for item in base.rglob("*"):
        if item.is_dir():
            images = list(item.glob("*.jpg")) + list(item.glob("*.jpeg")) + list(item.glob("*.png"))
            if len(images) >= 5:  # Valid class directory
                class_dirs.append(item)
    
    if not class_dirs:
        # Try direct subdirs
        for subdir in base.iterdir():
            if subdir.is_dir():
                images = list(subdir.glob("*.jpg")) + list(subdir.glob("*.jpeg")) + list(subdir.glob("*.png"))
                if images:
                    class_dirs.append(subdir)
    
    return class_dirs


if __name__ == "__main__":
    path = load_dataset()
    print(f"Dataset loaded at: {path}")
    dirs = find_image_directories(path)
    print(f"Found {len(dirs)} class directories")
