"""
Crop disease remedies, soil recommendations, and environmental guidance.
Supports Tomato, Potato, and Bell Pepper classes from PlantVillage-style folders.
Includes English and Kannada (ಕನ್ನಡ) remedy text.
"""


def normalize_disease_name(name):
    """Convert folder names like 'Tomato___Bacterial_spot' to 'Bacterial Spot'."""
    s = str(name)
    # Drop crop prefix before disease portion when present
    if "___" in s:
        s = s.split("___", 1)[1]
    s = s.replace(",", " ").replace("___", " ").replace("__", " ").replace("_", " ")
    s = " ".join(w.capitalize() for w in s.split() if w.lower() not in {"bell"})
    # Clean common leftovers like "Pepper Bell Bacterial Spot" -> handled via crop extract
    if s.lower().startswith("pepper "):
        s = s[7:].strip()
    return s.strip()


def get_crop_name(class_name):
    """Infer crop from dataset class / folder name."""
    d = str(class_name).lower()
    if "potato" in d:
        return "Potato"
    if "pepper" in d:
        return "Bell Pepper"
    if "tomato" in d:
        return "Tomato"
    return "Crop"


# Core remedies mapping (English + Kannada)
REMEDIES = {
    "healthy": {
        "remedies": (
            "No treatment needed. Continue regular care: proper watering, "
            "balanced fertilization, and routine pest monitoring."
        ),
        "remedies_kn": (
            "ಯಾವುದೇ ಚಿಕಿತ್ಸೆ ಅಗತ್ಯವಿಲ್ಲ. ನಿಯಮಿತ ನೀರಾವರಿ, ಸಮತೋಲಿತ ಗೊಬ್ಬರ "
            "ಮತ್ತು ಕೀಟಗಳ ನಿಗಾವಣೆಯನ್ನು ಮುಂದುವರಿಸಿ."
        ),
        "soil_recommendation": (
            "Well-drained loamy soil with pH 6.0-6.8. Add organic matter to improve structure."
        ),
        "environment_recommendation": (
            "Full sun (6-8 hours), moderate humidity (50-70%), warm temperatures (70-85°F)."
        ),
    },
    "bacterial spot": {
        "remedies": (
            "Apply copper-based bactericide/fungicide. Remove and destroy infected leaves. "
            "Avoid overhead watering. Use disease-free seeds and clean tools between plants."
        ),
        "remedies_kn": (
            "ತಾಮ್ರ ಆಧಾರಿತ ಔಷಧಿ ಸಿಂಪಡಿಸಿ. ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆದು ನಾಶಪಡಿಸಿ. "
            "ಮೇಲಿನಿಂದ ನೀರು ಹಾಕುವುದನ್ನು ತಪ್ಪಿಸಿ. ರೋಗರಹಿತ ಬೀಜ ಬಳಸಿ ಮತ್ತು ಸಾಧನಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ."
        ),
        "soil_recommendation": (
            "Well-drained fertile soil. Avoid replanting in previously infected soil; rotate crops."
        ),
        "environment_recommendation": (
            "Warm (75-90°F), humid conditions favor spread. Ensure good air circulation."
        ),
    },
    "early blight": {
        "remedies": (
            "Apply fungicide (chlorothalonil or copper). Remove infected leaves promptly. "
            "Mulch to prevent soil splash. Practice crop rotation for 2-3 years."
        ),
        "remedies_kn": (
            "ಶಿಲೀಂಧ್ರನಾಶಕ (ಕ್ಲೋರೋಥಲೋನಿಲ್ ಅಥವಾ ತಾಮ್ರ) ಸಿಂಪಡಿಸಿ. ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ಕೂಡಲೇ ತೆಗೆಯಿರಿ. "
            "ಮಣ್ಣು ಎಲೆಯ ಮೇಲೆ ಚಿಮುಕುವುದನ್ನು ತಡೆಯಲು ಮಲ್ಚ್ ಹಾಕಿ. ೨-೩ ವರ್ಷ ಬೆಳೆ ಪರಿವರ್ತನೆ ಮಾಡಿ."
        ),
        "soil_recommendation": (
            "Well-drained loamy soil with good organic matter. Avoid excess nitrogen."
        ),
        "environment_recommendation": (
            "Warm temperatures (75-85°F) and wet leaves promote infection. Water at the base."
        ),
    },
    "late blight": {
        "remedies": (
            "Apply fungicide (chlorothalonil, mancozeb) at first sign. Remove and destroy "
            "infected plants. Improve drainage and avoid prolonged leaf wetness."
        ),
        "remedies_kn": (
            "ಮೊದಲ ಲಕ್ಷಣ ಕಂಡ ಕೂಡಲೇ ಶಿಲೀಂಧ್ರನಾಶಕ (ಕ್ಲೋರೋಥಲೋನಿಲ್, ಮ್ಯಾಂಕೋಜೆಬ್) ಸಿಂಪಡಿಸಿ. "
            "ಸೋಂಕಿತ ಸಸ್ಯಗಳನ್ನು ತೆಗೆದು ನಾಶಪಡಿಸಿ. ನೀರು ಬಸಿದು ಹೋಗುವಂತೆ ನೋಡಿಕೊಳ್ಳಿ ಮತ್ತು ಎಲೆಗಳು "
            "ಹೆಚ್ಚು ಹೊತ್ತು ತೇವವಾಗದಂತೆ ಇರಿಸಿ."
        ),
        "soil_recommendation": (
            "Well-drained fertile soil. Avoid waterlogged conditions and poorly drained beds."
        ),
        "environment_recommendation": (
            "Cool (60-75°F) with high humidity favors late blight. Space plants for airflow."
        ),
    },
    "leaf mold": {
        "remedies": (
            "Apply sulfur or copper fungicide. Remove infected leaves. Improve air circulation. "
            "Prefer resistant varieties when available."
        ),
        "remedies_kn": (
            "ಗಂಧಕ ಅಥವಾ ತಾಮ್ರದ ಶಿಲೀಂಧ್ರನಾಶಕ ಸಿಂಪಡಿಸಿ. ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ. "
            "ಗಾಳಿ ಸಂಚಾರ ಹೆಚ್ಚಿಸಿ. ಸಾಧ್ಯವಾದರೆ ರೋಗ ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬೆಳೆಯಿರಿ."
        ),
        "soil_recommendation": (
            "Well-drained soil. Avoid excessive nitrogen which increases susceptibility."
        ),
        "environment_recommendation": (
            "High humidity (80%+) and moderate temps (70-80°F) favor disease."
        ),
    },
    "septoria leaf spot": {
        "remedies": (
            "Apply copper or chlorothalonil fungicide. Remove lower infected leaves. "
            "Mulch to reduce soil splash onto foliage."
        ),
        "remedies_kn": (
            "ತಾಮ್ರ ಅಥವಾ ಕ್ಲೋರೋಥಲೋನಿಲ್ ಶಿಲೀಂಧ್ರನಾಶಕ ಸಿಂಪಡಿಸಿ. ಕೆಳಗಿನ ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ. "
            "ಮಣ್ಣು ಎಲೆಯ ಮೇಲೆ ಬೀಳದಂತೆ ಮಲ್ಚ್ ಹಾಕಿ."
        ),
        "soil_recommendation": (
            "Well-drained soil. Rotate with non-solanaceous crops."
        ),
        "environment_recommendation": (
            "Warm (70-80°F) and humid conditions with wet foliage encourage spread."
        ),
    },
    "spider mites": {
        "remedies": (
            "Spray with insecticidal soap or neem oil. Introduce predatory mites if possible. "
            "Increase humidity slightly and remove heavily infested leaves."
        ),
        "remedies_kn": (
            "ಕೀಟನಾಶಕ ಸೋಪ್ ಅಥವಾ ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ. ಸಾಧ್ಯವಾದರೆ ಪರಭಕ್ಷಕ ಹುಳುಗಳನ್ನು ಬಿಡಿ. "
            "ಸ್ವಲ್ಪ ತೇವಾಂಶ ಹೆಚ್ಚಿಸಿ ಮತ್ತು ಹೆಚ್ಚು ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ."
        ),
        "soil_recommendation": (
            "Well-drained soil. Keep plants evenly watered to reduce stress that attracts mites."
        ),
        "environment_recommendation": (
            "Hot, dry conditions favor mites. Maintain moderate humidity around plants."
        ),
    },
    "tomato mosaic virus": {
        "remedies": (
            "No chemical cure. Remove and destroy infected plants. Control aphids. "
            "Use virus-free seeds and disinfect tools after handling plants."
        ),
        "remedies_kn": (
            "ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ ಇಲ್ಲ. ಸೋಂಕಿತ ಸಸ್ಯಗಳನ್ನು ತೆಗೆದು ನಾಶಪಡಿಸಿ. ಮೊಲೆಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸಿ. "
            "ವೈರಸ್-ರಹಿತ ಬೀಜ ಬಳಸಿ ಮತ್ತು ಸಾಧನಗಳನ್ನು ಸೋಂಕುರಹಿತಗೊಳಿಸಿ."
        ),
        "soil_recommendation": (
            "Well-drained soil. Avoid planting where tobacco or related solanaceous crops grew."
        ),
        "environment_recommendation": (
            "Spreads via sap, tools, and aphids. Warm conditions favor vector activity."
        ),
    },
    "target spot": {
        "remedies": (
            "Apply fungicide (chlorothalonil, mancozeb). Remove infected leaves. "
            "Improve airflow and avoid overhead irrigation."
        ),
        "remedies_kn": (
            "ಶಿಲೀಂಧ್ರನಾಶಕ (ಕ್ಲೋರೋಥಲೋನಿಲ್, ಮ್ಯಾಂಕೋಜೆಬ್) ಸಿಂಪಡಿಸಿ. ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ. "
            "ಗಾಳಿ ಸಂಚಾರ ಸುಧಾರಿಸಿ ಮತ್ತು ಮೇಲಿನಿಂದ ನೀರಾವರಿ ತಪ್ಪಿಸಿ."
        ),
        "soil_recommendation": (
            "Well-drained fertile soil. Crop rotation helps reduce inoculum."
        ),
        "environment_recommendation": (
            "Warm (75-85°F) and humid weather with prolonged leaf wetness promotes disease."
        ),
    },
    "tomato yellow leaf curl virus": {
        "remedies": (
            "Control whiteflies (primary vector) with insecticides or reflective mulch. "
            "Remove infected plants. Use resistant varieties when available."
        ),
        "remedies_kn": (
            "ಬಿಳಿ ನೊಣಗಳನ್ನು ಕೀಟನಾಶಕ ಅಥವಾ ಪ್ರತಿಫಲನ ಮಲ್ಚ್‌ನಿಂದ ನಿಯಂತ್ರಿಸಿ. "
            "ಸೋಂಕಿತ ಸಸ್ಯಗಳನ್ನು ತೆಗೆಯಿರಿ. ಸಾಧ್ಯವಾದರೆ ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ."
        ),
        "soil_recommendation": (
            "Well-drained soil. Keep plants vigorous to reduce secondary stress."
        ),
        "environment_recommendation": (
            "Warm conditions favor whiteflies. Use row covers early to exclude vectors."
        ),
    },
    "pepper bacterial spot": {
        "remedies": (
            "For bell pepper bacterial spot: apply copper sprays early, prune infected foliage, "
            "and avoid working plants when wet. Use certified disease-free transplants."
        ),
        "remedies_kn": (
            "ಕ್ಯಾಪ್ಸಿಕಂ ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಸ್ಪಾಟ್‌ಗೆ: ಬೇಗನೆ ತಾಮ್ರ ಸಿಂಪಡಿಸಿ, ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ಕತ್ತರಿಸಿ, "
            "ಸಸ್ಯಗಳು ತೇವವಾಗಿರುವಾಗ ಕೆಲಸ ಮಾಡಬೇಡಿ. ರೋಗರಹಿತ ಸಸಿಗಳನ್ನು ನೆಡಿರಿ."
        ),
        "soil_recommendation": (
            "Loose, well-drained soil with pH 6.0-6.8. Rotate away from peppers/tomatoes for 2+ years."
        ),
        "environment_recommendation": (
            "Warm humid weather spreads bacteria via splash. Space plants and water at soil level."
        ),
    },
    "pepper healthy": {
        "remedies": (
            "Bell pepper plant looks healthy. Maintain even watering, balanced NPK fertilizer, "
            "and weekly scouting for spots or soft lesions."
        ),
        "remedies_kn": (
            "ಕ್ಯಾಪ್ಸಿಕಂ ಸಸ್ಯ ಆರೋಗ್ಯಕರವಾಗಿದೆ. ಸಮತೋಲಿತ ನೀರಾವರಿ ಮತ್ತು ಗೊಬ್ಬರ ಮುಂದುವರಿಸಿ. "
            "ಪ್ರತಿ ವಾರ ಚುಕ್ಕೆಗಳು ಅಥವಾ ಮೃದು ಕಲೆಗಳಿಗಾಗಿ ಪರಿಶೀಲಿಸಿ."
        ),
        "soil_recommendation": (
            "Fertile, well-drained loam; keep soil consistently moist but not waterlogged."
        ),
        "environment_recommendation": (
            "Full sun, daytime 70-85°F. Provide airflow to keep leaves dry."
        ),
    },
    "potato early blight": {
        "remedies": (
            "For potato early blight: start protectant fungicides (chlorothalonil/mancozeb) at "
            "row closure. Remove lower yellowed leaves and destroy crop debris after harvest."
        ),
        "remedies_kn": (
            "ಆಲೂಗಡ್ಡೆ ಆರ್ಲಿ ಬ್ಲೈಟ್‌ಗೆ: ಸಾಲು ಮುಚ್ಚಿದಾಗಿನಿಂದ ಶಿಲೀಂಧ್ರನಾಶಕ "
            "(ಕ್ಲೋರೋಥಲೋನಿಲ್/ಮ್ಯಾಂಕೋಜೆಬ್) ಪ್ರಾರಂಭಿಸಿ. ಕೆಳಗಿನ ಹಳದಿ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ ಮತ್ತು "
            "ಕೊಯ್ಲಿನ ನಂತರ ಅವಶೇಷಗಳನ್ನು ನಾಶಪಡಿಸಿ."
        ),
        "soil_recommendation": (
            "Well-drained sandy loam. Avoid planting potatoes in the same bed year after year."
        ),
        "environment_recommendation": (
            "Warm dry days with cool nights favor early blight. Irrigate early so foliage dries."
        ),
    },
    "potato late blight": {
        "remedies": (
            "For potato late blight: apply systemic/protectant fungicides immediately, remove "
            "infected plants, and hill soil over tubers. Do not leave cull piles nearby."
        ),
        "remedies_kn": (
            "ಆಲೂಗಡ್ಡೆ ಲೇಟ್ ಬ್ಲೈಟ್‌ಗೆ: ತಕ್ಷಣ ಶಿಲೀಂಧ್ರನಾಶಕ ಸಿಂಪಡಿಸಿ, ಸೋಂಕಿತ ಸಸ್ಯಗಳನ್ನು ತೆಗೆಯಿರಿ, "
            "ಗೆಡ್ಡೆಗಳ ಮೇಲೆ ಮಣ್ಣು ಹಾಕಿ. ಹತ್ತಿರದಲ್ಲಿ ತಿರಸ್ಕೃತ ಗೆಡ್ಡೆಗಳನ್ನು ಬಿಡಬೇಡಿ."
        ),
        "soil_recommendation": (
            "Raised, well-drained beds. Avoid standing water that keeps foliage wet overnight."
        ),
        "environment_recommendation": (
            "Cool wet weather (60-70°F) drives outbreaks. Improve airflow and reduce leaf wetness."
        ),
    },
    "potato healthy": {
        "remedies": (
            "Potato foliage appears healthy. Continue hilling, balanced fertility, and "
            "preventive scouting especially during humid stretches."
        ),
        "remedies_kn": (
            "ಆಲೂಗಡ್ಡೆ ಎಲೆಗಳು ಆರೋಗ್ಯಕರವಾಗಿವೆ. ಮಣ್ಣು ಹಾಕುವುದು ಮತ್ತು ಸಮತೋಲಿತ ಗೊಬ್ಬರ ಮುಂದುವರಿಸಿ. "
            "ತೇವಾಂಶ ಹೆಚ್ಚಿರುವಾಗ ವಿಶೇಷವಾಗಿ ಗಮನವಿಡಿ."
        ),
        "soil_recommendation": (
            "Loose, well-drained soil with moderate fertility; avoid excess nitrogen late season."
        ),
        "environment_recommendation": (
            "Cool to mild temperatures with good sun. Keep foliage dry when possible."
        ),
    },
}

DEFAULT_REMEDIES_KN = (
    "ಸ್ಥಳೀಯ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ. ಕಾಣುವ ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆಯಿರಿ. "
    "ಶಿಲೀಂಧ್ರ ರೋಗವಾದರೆ ವ್ಯಾಪಕ ಶಿಲೀಂಧ್ರನಾಶಕ ಬಳಸಿ. ಗಾಳಿ ಸಂಚಾರ ಸುಧಾರಿಸಿ ಮತ್ತು "
    "ಮೇಲಿನಿಂದ ನೀರು ಹಾಕುವುದನ್ನು ತಪ್ಪಿಸಿ."
)

SEVERITY_LEVELS = {
    "healthy": "None",
    "bacterial spot": "High",
    "early blight": "Medium",
    "late blight": "Very High",
    "leaf mold": "Medium",
    "septoria leaf spot": "High",
    "spider mites": "Medium",
    "tomato mosaic virus": "Very High",
    "target spot": "Medium",
    "tomato yellow leaf curl virus": "Very High",
    "pepper bacterial spot": "High",
    "pepper healthy": "None",
    "potato early blight": "Medium",
    "potato late blight": "Very High",
    "potato healthy": "None",
}

# Kannada display names for each matched disease key
DISEASE_NAMES_KN = {
    "healthy": "ಆರೋಗ್ಯಕರ ಸಸ್ಯ",
    "bacterial spot": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಸ್ಪಾಟ್ (ಬ್ಯಾಕ್ಟೀರಿಯಾ ಕಲೆ ರೋಗ)",
    "early blight": "ಆರ್ಲಿ ಬ್ಲೈಟ್ (ಪೂರ್ವ ಮುದುರು ರೋಗ)",
    "late blight": "ಲೇಟ್ ಬ್ಲೈಟ್ (ವಿಳಂಬ ಮುದುರು ರೋಗ)",
    "leaf mold": "ಲೀಫ್ ಮೋಲ್ಡ್ (ಎಲೆ ಅಚ್ಚು ರೋಗ)",
    "septoria leaf spot": "ಸೆಪ್ಟೋರಿಯಾ ಲೀಫ್ ಸ್ಪಾಟ್ (ಸೆಪ್ಟೋರಿಯಾ ಎಲೆ ಕಲೆ)",
    "spider mites": "ಸ್ಪೈಡರ್ ಮೈಟ್‌ಗಳು (ಜೇಡೆ ಹುಳುಗಳು)",
    "tomato mosaic virus": "ಟೊಮೇಟೊ ಮೊಸಾಯಿಕ್ ವೈರಸ್",
    "target spot": "ಟಾರ್ಗೆಟ್ ಸ್ಪಾಟ್ (ಗುರಿ ಕಲೆ ರೋಗ)",
    "tomato yellow leaf curl virus": "ಟೊಮೇಟೊ ಯೆಲ್ಲೋ ಲೀಫ್ ಕರ್ಲ್ ವೈರಸ್ (ಹಳದಿ ಎಲೆ ಸುರುಳಿ ವೈರಸ್)",
    "pepper bacterial spot": "ಕ್ಯಾಪ್ಸಿಕಂ ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಸ್ಪಾಟ್",
    "pepper healthy": "ಕ್ಯಾಪ್ಸಿಕಂ ಆರೋಗ್ಯಕರ ಸಸ್ಯ",
    "potato early blight": "ಆಲೂಗಡ್ಡೆ ಆರ್ಲಿ ಬ್ಲೈಟ್",
    "potato late blight": "ಆಲೂಗಡ್ಡೆ ಲೇಟ್ ಬ್ಲೈಟ್",
    "potato healthy": "ಆಲೂಗಡ್ಡೆ ಆರೋಗ್ಯಕರ ಸಸ್ಯ",
}

CROP_NAMES_KN = {
    "Potato": "ಆಲೂಗಡ್ಡೆ",
    "Bell Pepper": "ಕ್ಯಾಪ್ಸಿಕಂ",
    "Tomato": "ಟೊಮೇಟೊ",
    "Crop": "ಬೆಳೆ",
}


def _normalize_key(disease_name):
    d = disease_name.lower().strip()
    d = d.replace(",", " ").replace("___", " ").replace("__", " ").replace("_", " ")
    d = " ".join(d.split())
    return d


def _match_key(d):
    """Return the best REMEDIES key for a normalized disease string."""
    # Prefer crop-specific keys first
    if "pepper" in d and "bacterial" in d and "spot" in d:
        return "pepper bacterial spot"
    if "pepper" in d and "healthy" in d:
        return "pepper healthy"
    if "potato" in d and "early" in d and "blight" in d:
        return "potato early blight"
    if "potato" in d and "late" in d and "blight" in d:
        return "potato late blight"
    if "potato" in d and "healthy" in d:
        return "potato healthy"

    for key in REMEDIES:
        if key in d or d in key:
            return key

    if "healthy" in d:
        return "healthy"
    if "bacterial" in d and "spot" in d:
        return "bacterial spot"
    if "early" in d and "blight" in d:
        return "early blight"
    if "late" in d and "blight" in d:
        return "late blight"
    if "mold" in d:
        return "leaf mold"
    if "septoria" in d:
        return "septoria leaf spot"
    if "spider" in d or "mite" in d:
        return "spider mites"
    if "mosaic" in d:
        return "tomato mosaic virus"
    if "target" in d and "spot" in d:
        return "target spot"
    if "yellow" in d or "curl" in d:
        return "tomato yellow leaf curl virus"
    return None


def get_severity_for_disease(disease_name):
    """Return disease severity based on normalized disease name."""
    d = _normalize_key(disease_name)
    key = _match_key(d)
    if key and key in SEVERITY_LEVELS:
        return SEVERITY_LEVELS[key]
    return "Unknown"


def get_disease_name_kn(disease_name):
    """Return Kannada disease name for a class / disease string."""
    d = _normalize_key(disease_name)
    key = _match_key(d)
    if key and key in DISEASE_NAMES_KN:
        return DISEASE_NAMES_KN[key]
    return "ಅಜ್ಞಾತ ರೋಗ"


def get_crop_name_kn(crop_name):
    """Return Kannada crop name."""
    return CROP_NAMES_KN.get(crop_name, CROP_NAMES_KN["Crop"])


def get_remedies_for_disease(disease_name):
    """
    Get remedies for a disease. Handles various naming formats from dataset.
    Returns dict with remedies, remedies_kn, soil_recommendation, environment_recommendation.
    """
    d = _normalize_key(disease_name)
    key = _match_key(d)
    if key and key in REMEDIES:
        data = REMEDIES[key].copy()
        data.setdefault("remedies_kn", DEFAULT_REMEDIES_KN)
        return data

    return {
        "remedies": (
            "Consult a local agricultural expert. Remove visibly infected leaves. "
            "Apply broad-spectrum fungicide if fungal. Improve air circulation and "
            "avoid overhead watering."
        ),
        "remedies_kn": DEFAULT_REMEDIES_KN,
        "soil_recommendation": (
            "Well-drained loamy soil with pH 6.0-6.8. Ensure proper drainage."
        ),
        "environment_recommendation": (
            "Full sun, moderate humidity. Avoid prolonged leaf wetness."
        ),
    }
