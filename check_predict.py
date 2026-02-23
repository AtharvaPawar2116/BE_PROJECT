import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib
import os, json
from datetime import datetime

# =========================
# MODEL LOAD
# =========================
MODEL_PATH = "model_outputs/crop_recommendation_model.pkl"
model = joblib.load(MODEL_PATH)

# =========================
# JSON FILE (Crop Map)
# =========================
CROP_MAP_JSON_PATH = "crop_marathi_map.json"

DEFAULT_CROP_MARATHI_MAP = {
    "amaranthus": "तांदुळजा",
    "green banana": "कच्ची केळी",
    "banana": "केळी",
    "ladies finger": "भेंडी",
    "bitter gourd": "कारले",
    "bottle gourd": "दुधी भोपळा",
    "brinjal": "वांगी",
    "cabbage": "कोबी",
    "carrot": "गाजर",
    "cauliflower": "फुलकोबी",
    "cluster beans": "गवार",
    "cowpea": "चवळी",
    "cucumber": "काकडी",
    "drumstick": "शेवगा",
    "ginger": "आले",
    "green chilli": "हिरवी मिरची",
    "garlic": "लसूण",
    "onion": "कांदा",
    "potato": "बटाटा",
    "tomato": "टोमॅटो",
    "pumpkin": "भोपळा",
    "raddish": "मुळा",
    "ridge gourd": "दोडका",
    "sponge gourd": "घोसाळे",
    "snakeguard": "पडवळ",
    "tinda": "टिंडा",
    "sweet potato": "रताळे",
    "spinach": "पालक",
    "methi leaves": "मेथी",
    "coriander": "कोथिंबीर",
    "peas": "वाटाणे",
    "peas cod": "वाटाणा शेंग",
    "beans": "शेंग",
    "french beans": "फ्रेंच बीन्स",
    "capsicum": "ढोबळी मिरची",

    # Fruits
    "apple": "सफरचंद",
    "orange": "संत्रे",
    "grapes": "द्राक्षे",
    "papaya": "पपई",
    "pomegranate": "डाळिंब",
    "guava": "पेरू",
    "lemon": "लिंबू",
    "water melon": "टरबूज",
    "sweet lime": "मोसंबी",
    "pineapple": "अननस",
    "sapota": "चिकू",
    "mango": "आंबा",
    "zizyphus": "बोर",

    # Cereals & Pulses
    "paddy": "भात",
    "rice": "तांदूळ",
    "wheat": "गहू",
    "wheat atta": "गव्हाचे पीठ",
    "maize": "मका",
    "jowar": "ज्वारी",
    "bajra": "बाजरी",
    "ragi": "नाचणी",
    "barley": "जव",
    "lentil": "मसूर",
    "masur dal": "मसूर डाळ",
    "bengal gram": "हरभरा",
    "black gram": "उडीद",
    "green gram": "मूग",
    "red gram": "तूर",
    "chana dal": "चना डाळ",
    "tur dal": "तूर डाळ",
    "urd dal": "उडीद डाळ",

    # Oil & Commercial Crops
    "groundnut": "भुईमूग",
    "soyabean": "सोयाबीन",
    "mustard": "मोहरी",
    "sesamum": "तीळ",
    "cotton": "कापूस",
    "jute": "ताग",
    "castor seed": "एरंड",
    "tobacco": "तंबाखू",

    # Plantation
    "coconut": "नारळ",
    "copra": "खोबरे",
    "arecanut": "सुपारी",
    "cashewnuts": "काजू",
    "rubber": "रबर",

    # Others
    "turmeric": "हळद",
    "jaggery": "गूळ",
    "sugar": "साखर",
    "fish": "मासे",
    "wood": "लाकूड",
    "leafy vegetable": "पालेभाजी"
}

def ensure_crop_map_json():
    """Create crop_marathi_map.json if not exists."""
    if not os.path.exists(CROP_MAP_JSON_PATH):
        with open(CROP_MAP_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CROP_MARATHI_MAP, f, ensure_ascii=False, indent=2)

def load_crop_map():
    ensure_crop_map_json()
    with open(CROP_MAP_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

CROP_MARATHI_MAP = load_crop_map()

# =========================
# State & Soil Lists / Maps
# =========================
state_marathi_list = [
    "अंदमान आणि निकोबार","आंध्र प्रदेश","आसाम","छत्तीसगड","गोवा","गुजरात","हरियाणा",
    "हिमाचल प्रदेश","जम्मू आणि काश्मीर","कर्नाटक","केरळ","मध्य प्रदेश","महाराष्ट्र",
    "मणिपूर","मेघालय","नागालँड","ओडिशा","पाँडिचेरी","पंजाब","राजस्थान","तामिळनाडू",
    "तेलंगणा","त्रिपुरा","उत्तर प्रदेश","उत्तराखंड","पश्चिम बंगाल"
]

STATE_ENGLISH_MAP = {
    "अंदमान आणि निकोबार": "Andaman and Nicobar",
    "आंध्र प्रदेश": "Andhra Pradesh",
    "आसाम": "Assam",
    "छत्तीसगड": "Chattisgarh",
    "गोवा": "Goa",
    "गुजरात": "Gujarat",
    "हरियाणा": "Haryana",
    "हिमाचल प्रदेश": "Himachal Pradesh",
    "जम्मू आणि काश्मीर": "Jammu and Kashmir",
    "कर्नाटक": "Karnataka",
    "केरळ": "Kerala",
    "मध्य प्रदेश": "Madhya Pradesh",
    "महाराष्ट्र": "Maharashtra",
    "मणिपूर": "Manipur",
    "मेघालय": "Meghalaya",
    "नागालँड": "Nagaland",
    "ओडिशा": "Odisha",
    "पाँडिचेरी": "Pondicherry",
    "पंजाब": "Punjab",
    "राजस्थान": "Rajasthan",
    "तामिळनाडू": "Tamil Nadu",
    "तेलंगणा": "Telangana",
    "त्रिपुरा": "Tripura",
    "उत्तर प्रदेश": "Uttar Pradesh",
    "उत्तराखंड": "Uttrakhand",
    "पश्चिम बंगाल": "West Bengal"
}

SOIL_MARATHI_LIST = [
    "वालुकामय माती","लाल माती","लेटराइट माती","चिकणमाती","वाळवंटी माती",
    "वालुकामय दोमट माती","गाळाची माती","वालुकामय चिकणमाती","काळी माती",
    "रेगूर माती","इनसेप्टिसोल माती","दुमट माती","डेल्टा गाळाची माती","डोंगराळ माती"
]

SOIL_ENGLISH_MAP = {
    "वालुकामय माती": "Sandy soil",
    "लाल माती": "Red soil",
    "लेटराइट माती": "Laterite soil",
    "चिकणमाती": "Clayey soils",
    "वाळवंटी माती": "Desert soil",
    "वालुकामय दोमट माती": "Sandy loam",
    "गाळाची माती": "Alluvial soil",
    "वालुकामय चिकणमाती": "Sandy Clay loam",
    "काळी माती": "Black soil",
    "रेगूर माती": "Regur soil",
    "इनसेप्टिसोल माती": "Inceptisols",
    "दुमट माती": "Loamy soil",
    "डेल्टा गाळाची माती": "Delta alluvium",
    "डोंगराळ माती": "Mountain soil"
}

# =========================
# Soil Details + Steps (Report)
# =========================
SOIL_GUIDE = {
    "Sandy soil": {
        "details": "पाणी लवकर निचरा होते, पोषकद्रव्य धरून ठेवण्याची क्षमता कमी. सेंद्रिय पदार्थ आणि मल्चिंग गरजेचे.",
        "steps": [
            "कंपोस्ट/शेणखत भरपूर मिसळा (ओलावा टिकवण्यासाठी).",
            "ड्रिप/वारंवार हलके सिंचन करा.",
            "खते विभागून द्या (split application).",
            "मल्चिंग करा (तण कमी + ओलावा टिकतो)."
        ]
    },
    "Black soil": {
        "details": "चिकणमाती जास्त; पाणी धरून ठेवते पण पाणी साचू शकते. निचरा महत्त्वाचा.",
        "steps": [
            "निचरा चांगला ठेवा (पाणी साचू देऊ नका).",
            "सेंद्रिय खत मिसळून माती भुसभुशीत करा.",
            "पेरणीपूर्वी माती परीक्षण करून pH/NPK तपासा."
        ]
    },
    "Alluvial soil": {
        "details": "सुपीक माती; पाणी धरणे/निचरा मध्यम. संतुलित NPK व्यवस्थापन केल्यास उत्पादन वाढते.",
        "steps": [
            "माती परीक्षण करा आणि NPK शिफारशीनुसार द्या.",
            "सिंचन नियोजन: अति सिंचन टाळा.",
            "तण/कीड नियंत्रण नियमित करा."
        ]
    },
    "Red soil": {
        "details": "सेंद्रिय पदार्थ कमी असू शकतो; सेंद्रिय खत आणि संतुलित खत व्यवस्थापन आवश्यक.",
        "steps": [
            "कंपोस्ट/वर्मी-कंपोस्ट वाढवा.",
            "नत्र (N) व्यवस्थापन split doses मध्ये करा.",
            "ओलावा टिकवण्यासाठी मल्चिंग करा."
        ]
    },
    "Laterite soil": {
        "details": "आम्लीय (acidic) असू शकते; पोषकद्रव्य कमी. सेंद्रिय पदार्थ + गरजेनुसार चुना (तज्ज्ञ सल्ल्याने).",
        "steps": [
            "pH तपासा; खूप आम्लीय असेल तर liming (तज्ज्ञ सल्ल्याने).",
            "कंपोस्ट/वर्मी-कंपोस्ट वापरा.",
            "सूक्ष्मअन्नद्रव्य गरजेप्रमाणे द्या."
        ]
    }
}

# Crop specific quick tips
CROP_GUIDE = {
    "tomato": [
        "रोपे लावताना योग्य अंतर ठेवा; स्टेकिंग/सपोर्ट द्या.",
        "फुलोऱ्यावर बुरशी/किडीचे निरीक्षण करा.",
        "पाणी नियमित द्या पण पाणी साचू देऊ नका."
    ],
    "potato": [
        "सरी-वरंबा पद्धत उपयुक्त; माती चढवणे (earthing up) करा.",
        "जास्त पाणी टाळा; रोग (ब्लाइट) निरीक्षण करा."
    ],
    "paddy": [
        "पाण्याचे नियोजन करा; रोप लावणी/थेट पेरणी योग्य पद्धतीने करा.",
        "तण नियंत्रण सुरुवातीच्या टप्प्यात महत्वाचे."
    ],
    "wheat": [
        "वेळेवर पेरणी करा; टॉप ड्रेसिंग योग्य वेळी द्या.",
        "अति पाणी टाळा; मध्यम सिंचन ठेवा."
    ],
    "soyabean": [
        "पाणी साचू देऊ नका; बीजप्रक्रिया (Rhizobium/PSB) फायदेशीर.",
        "सुरुवातीचे 30-45 दिवस तणमुक्त ठेवा."
    ],
    "cotton": [
        "सुरुवातीच्या अवस्थेत तण नियंत्रण आणि कीड निरीक्षण (बोलवर्म/मावा) करा.",
        "संतुलित खत व्यवस्थापन ठेवा."
    ]
}

# =========================
# REPORT BUILD + SAVE
# =========================
def build_report(data_dict, crop_en, crop_mr):
    state_mr = state.get()
    soil_mr = soil_type.get()
    state_en = STATE_ENGLISH_MAP.get(state_mr, state_mr)
    soil_en = SOIL_ENGLISH_MAP.get(soil_mr, soil_mr)

    soil_info = SOIL_GUIDE.get(soil_en, {
        "details": "या मातीसाठी सामान्य शेती पद्धती लागू करा.",
        "steps": ["माती परीक्षण करा.", "सेंद्रिय खत वाढवा.", "सिंचन/निचरा योग्य ठेवा."]
    })

    crop_steps = CROP_GUIDE.get(crop_en, [
        "माती परीक्षण करून स्थानिक शिफारशीनुसार खत व्यवस्थापन करा.",
        "योग्य बियाणे/रोपे निवडा.",
        "सिंचन, तण नियंत्रण, कीड/रोग निरीक्षण नियमित करा."
    ])

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    soil_steps_txt = "\n".join([f"{i+1}. {s}" for i, s in enumerate(soil_info["steps"])])
    crop_steps_txt = "\n".join([f"{i+1}. {s}" for i, s in enumerate(crop_steps)])

    report = f"""
===================== CROP RECOMMENDATION REPORT =====================
Generated On: {now}

INPUTS:
- State (Marathi): {state_mr}
- State (English): {state_en}
- Soil Type (Marathi): {soil_mr}
- Soil Type (English): {soil_en}

- N (Nitrogen): {data_dict['N_SOIL'][0]}
- P (Phosphorus): {data_dict['P_SOIL'][0]}
- K (Potassium): {data_dict['K_SOIL'][0]}
- Temperature (°C): {data_dict['TEMPERATURE'][0]}
- Humidity (%): {data_dict['HUMIDITY'][0]}
- pH: {data_dict['ph'][0]}
- Rainfall (mm): {data_dict['RAINFALL'][0]}

RECOMMENDED CROP:
- English: {crop_en}
- Marathi: {crop_mr}

SOIL DETAILS:
{soil_info['details']}

STEP-BY-STEP (Soil Work Plan):
{soil_steps_txt}

STEP-BY-STEP (Crop Work Plan):
{crop_steps_txt}

NOTES:
- हा रिपोर्ट general guidance आहे.
- अचूक बियाणे प्रमाण, खत डोस, आणि फवारणीसाठी स्थानिक कृषी विभाग/तज्ज्ञ सल्ला घ्या.
======================================================================
""".strip()
    return report

def save_report(report_text, crop_en):
    os.makedirs("reports", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("reports", f"{crop_en}_report_{ts}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    return file_path

# =========================
# GUI SETUP
# =========================
root = tk.Tk()
root.title("पीक शिफारस प्रणाली")
root.geometry("900x600")
root.configure(bg="#2e7d32")

# Variables
state = tk.StringVar()
soil_type = tk.StringVar()
n_soil = tk.DoubleVar()
p_soil = tk.DoubleVar()
k_soil = tk.DoubleVar()
temperature = tk.DoubleVar()
humidity = tk.DoubleVar()
ph = tk.DoubleVar()
rainfall = tk.DoubleVar()

# =========================
# Predict function
# =========================
def predict_crop():
    try:
        data = {
            "STATE": [STATE_ENGLISH_MAP[state.get()]],
            "SOIL_TYPE": [SOIL_ENGLISH_MAP[soil_type.get()]],
            "N_SOIL": [float(n_soil.get())],
            "P_SOIL": [float(p_soil.get())],
            "K_SOIL": [float(k_soil.get())],
            "TEMPERATURE": [float(temperature.get())],
            "HUMIDITY": [float(humidity.get())],
            "ph": [float(ph.get())],
            "RAINFALL": [float(rainfall.get())]
        }
    except Exception:
        messagebox.showerror("Error", "कृपया सर्व value योग्य प्रकारे भरा (numbers).")
        return

    df = pd.DataFrame(data)

    # Predict English crop
    crop_en = str(model.predict(df)[0]).strip().lower()

    # Marathi crop (from JSON)
    crop_mr = CROP_MARATHI_MAP.get(crop_en, crop_en)

    # Show on UI
    result_label.config(
        text=f"शिफारस केलेले पीक : {crop_mr}",
        bg="#1b5e20",
        fg="white"
    )

    # Auto-generate report
    report_text = build_report(data, crop_en, crop_mr)
    report_path = save_report(report_text, crop_en)

    messagebox.showinfo("Report Generated", f"TXT Report Saved:\n{report_path}\n\n(फोल्डर: reports/)")

# =========================
# Frame
# =========================
frame = tk.LabelFrame(
    root,
    text="माती व हवामान माहिती भरा",
    font=("Arial", 16, "bold"),
    bg="#2e7d32",
    fg="white",
    padx=20,
    pady=20
)
frame.pack(pady=20)

# Helper Functions
def add_label(text, row):
    tk.Label(
        frame,
        text=text,
        bg="#2e7d32",
        fg="white",
        font=("Arial", 12)
    ).grid(row=row, column=0, pady=5, sticky="w")

def add_entry(var, row):
    tk.Entry(frame, textvariable=var, width=20).grid(row=row, column=1, pady=5)

def add_combo(var, values, row):
    cb = ttk.Combobox(frame, textvariable=var, values=values, width=18, state="readonly")
    cb.grid(row=row, column=1, pady=5)
    cb.current(0)

# Input Fields (Marathi)
add_label("राज्य", 0); add_combo(state, state_marathi_list, 0)
add_label("मातीचा प्रकार", 1); add_combo(soil_type, SOIL_MARATHI_LIST, 1)

add_label("नायट्रोजन (N)", 2); add_entry(n_soil, 2)
add_label("फॉस्फरस (P)", 3); add_entry(p_soil, 3)
add_label("पोटॅशियम (K)", 4); add_entry(k_soil, 4)
add_label("तापमान (°C)", 5); add_entry(temperature, 5)
add_label("आर्द्रता (%)", 6); add_entry(humidity, 6)
add_label("मातीचा pH", 7); add_entry(ph, 7)
add_label("पर्जन्यमान (मिमी)", 8); add_entry(rainfall, 8)

# Button
tk.Button(
    root,
    text="पीक शिफारस करा + रिपोर्ट तयार करा",
    command=predict_crop,
    font=("Arial", 14, "bold"),
    bg="#ff9800",
    fg="black",
    width=28
).pack(pady=20)

# Result Label
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 15, "bold"),
    bg="#2e7d32",
    fg="white",
    pady=20
)
result_label.pack()

root.mainloop()
