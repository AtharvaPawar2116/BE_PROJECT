import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib
import os, json
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import quote
from datetime import datetime

# =========================
# MODEL LOAD
# =========================
MODEL_PATH = "model_outputs/crop_recommendation_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    MODEL_LOAD_ERROR = str(e)
else:
    MODEL_LOAD_ERROR = ""

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

# महाराष्ट्रातील सर्व जिल्हे (तालुके API मधून)
MAHARASHTRA_DISTRICTS = [
    "Ahmednagar", "Akola", "Amravati", "Beed", "Bhandara", "Buldhana", "Chandrapur",
    "Chhatrapati Sambhajinagar", "Dhule", "Gadchiroli", "Gondia", "Hingoli", "Jalgaon",
    "Jalna", "Kolhapur", "Latur", "Mumbai City", "Mumbai Suburban", "Nagpur", "Nanded",
    "Nandurbar", "Nashik", "Osmanabad", "Palghar", "Parbhani", "Pune", "Raigad",
    "Ratnagiri", "Sangli", "Satara", "Sindhudurg", "Solapur", "Thane", "Wardha",
    "Washim", "Yavatmal"
]

DISTRICT_ENGLISH_MAP = {
    "अहमदनगर": "Ahmednagar", "अकोला": "Akola", "अमरावती": "Amravati", "बीड": "Beed",
    "भंडारा": "Bhandara", "बुलढाणा": "Buldhana", "चंद्रपूर": "Chandrapur",
    "छत्रपती संभाजीनगर": "Chhatrapati Sambhajinagar", "धुळे": "Dhule", "गडचिरोली": "Gadchiroli",
    "गोंदिया": "Gondia", "हिंगोली": "Hingoli", "जळगाव": "Jalgaon", "जालना": "Jalna",
    "कोल्हापूर": "Kolhapur", "लातूर": "Latur", "मुंबई शहर": "Mumbai City",
    "मुंबई उपनगर": "Mumbai Suburban", "नागपूर": "Nagpur", "नांदेड": "Nanded",
    "नंदुरबार": "Nandurbar", "नाशिक": "Nashik", "उस्मानाबाद": "Osmanabad", "पालघर": "Palghar",
    "परभणी": "Parbhani", "पुणे": "Pune", "रायगड": "Raigad", "रत्नागिरी": "Ratnagiri",
    "सांगली": "Sangli", "सातारा": "Satara", "सिंधुदुर्ग": "Sindhudurg", "सोलापूर": "Solapur",
    "ठाणे": "Thane", "वर्धा": "Wardha", "वाशीम": "Washim", "यवतमाळ": "Yavatmal"
}

DISTRICT_MARATHI_MAP = {v: k for k, v in DISTRICT_ENGLISH_MAP.items()}

# Offline fallback taluka map (works without external taluka API)
MAHARASHTRA_TALUKAS = {
    "Ahmednagar": ["Akole", "Jamkhed", "Karjat", "Kopargaon", "Nagar", "Nevasa", "Parner", "Pathardi", "Rahata", "Rahuri", "Sangamner", "Shevgaon", "Shrigonda", "Shrirampur"],
    "Akola": ["Akola", "Akot", "Balapur", "Barshitakli", "Murtizapur", "Patur", "Telhara"],
    "Amravati": ["Achalpur", "Amravati", "Anjangaon Surji", "Bhatkuli", "Chandur Bazar", "Chandur Railway", "Daryapur", "Dhamangaon Railway", "Morshi", "Nandgaon Khandeshwar", "Teosa", "Warud"],
    "Beed": ["Ambejogai", "Ashti", "Beed", "Dharur", "Georai", "Kaij", "Majalgaon", "Parli", "Patoda", "Shirur Kasar", "Wadwani"],
    "Bhandara": ["Bhandara", "Lakhandur", "Lakhani", "Mohadi", "Pauni", "Sakoli", "Tumsar"],
    "Buldhana": ["Buldhana", "Chikhli", "Deulgaon Raja", "Jalgaon Jamod", "Khamgaon", "Lonar", "Malkapur", "Mehkar", "Motala", "Nandura", "Sangrampur", "Shegaon", "Sindkhed Raja"],
    "Chandrapur": ["Ballarpur", "Bhadravati", "Brahmapuri", "Chandrapur", "Chimur", "Gondpipri", "Jiwati", "Korpana", "Mul", "Nagbhid", "Pombhurna", "Rajura", "Sawali", "Sindewahi", "Warora"],
    "Chhatrapati Sambhajinagar": ["Aurangabad", "Gangapur", "Kannad", "Khuldabad", "Paithan", "Phulambri", "Sillod", "Soegaon", "Vaijapur"],
    "Dhule": ["Dhule", "Sakri", "Shirpur", "Sindkhede"],
    "Gadchiroli": ["Aheri", "Armori", "Bhamragad", "Chamorshi", "Dhanora", "Etapalli", "Gadchiroli", "Korchi", "Kurkheda", "Mulchera", "Sironcha"],
    "Gondia": ["Amgaon", "Arjuni Morgaon", "Deori", "Gondia", "Goregaon", "Sadak Arjuni", "Salekasa", "Tirora"],
    "Hingoli": ["Aundha Nagnath", "Basmath", "Hingoli", "Kalamnuri", "Sengaon"],
    "Jalgaon": ["Amalner", "Bhadgaon", "Bhusawal", "Bodwad", "Chalisgaon", "Chopda", "Dharangaon", "Erandol", "Jalgaon", "Jamner", "Muktainagar", "Pachora", "Parola", "Raver", "Yawal"],
    "Jalna": ["Ambad", "Badnapur", "Bhokardan", "Ghansawangi", "Jafferabad", "Jalna", "Mantha", "Partur"],
    "Kolhapur": ["Ajra", "Bavda", "Bhudargad", "Chandgad", "Gadhinglaj", "Hatkanangale", "Kagal", "Karvir", "Panhala", "Radhanagari", "Shahuwadi", "Shirol"],
    "Latur": ["Ahmadpur", "Ausa", "Chakur", "Deoni", "Jalkot", "Latur", "Nilanga", "Renapur", "Shirur Anantpal", "Udgir"],
    "Mumbai City": ["Mumbai"],
    "Mumbai Suburban": ["Andheri", "Borivali", "Kurla"],
    "Nagpur": ["Bhiwapur", "Hingna", "Kalameshwar", "Kamptee", "Katol", "Kuhi", "Mauda", "Nagpur Rural", "Narkhed", "Parseoni", "Ramtek", "Saoner", "Umred"],
    "Nanded": ["Ardhapur", "Bhokar", "Biloli", "Deglur", "Dharmabad", "Hadgaon", "Himayatnagar", "Kandhar", "Kinwat", "Loha", "Mahur", "Mudkhed", "Mukhed", "Naigaon", "Nanded", "Umri"],
    "Nandurbar": ["Akkalkuwa", "Akrani", "Nandurbar", "Nawapur", "Shahada", "Taloda"],
    "Nashik": ["Baglan", "Chandwad", "Deola", "Dindori", "Igatpuri", "Kalwan", "Malegaon", "Nandgaon", "Nashik", "Niphad", "Peth", "Sinnar", "Surgana", "Trimbakeshwar", "Yeola"],
    "Osmanabad": ["Bhoom", "Kalamb", "Lohara", "Osmanabad", "Paranda", "Tuljapur", "Umarga", "Washi"],
    "Palghar": ["Dahanu", "Jawhar", "Mokhada", "Palghar", "Talasari", "Vasai", "Vikramgad", "Wada"],
    "Parbhani": ["Gangakhed", "Jintur", "Manwath", "Palam", "Parbhani", "Pathri", "Purna", "Sailu", "Sonpeth"],
    "Pune": ["Ambegaon", "Baramati", "Bhor", "Daund", "Haveli", "Indapur", "Junnar", "Khed", "Mawal", "Mulshi", "Purandar", "Shirur", "Velhe"],
    "Raigad": ["Alibag", "Karjat", "Khalapur", "Mahad", "Mangaon", "Mhasla", "Murud", "Panvel", "Pen", "Poladpur", "Roha", "Shrivardhan", "Sudhagad", "Tala", "Uran"],
    "Ratnagiri": ["Chiplun", "Dapoli", "Guhagar", "Khed", "Lanja", "Mandangad", "Rajapur", "Ratnagiri", "Sangameshwar"],
    "Sangli": ["Atpadi", "Jat", "Kadegaon", "Kavathemahankal", "Khanapur", "Miraj", "Palus", "Shirala", "Tasgaon", "Walwa"],
    "Satara": ["Jaoli", "Karad", "Khandala", "Khatav", "Koregaon", "Mahabaleshwar", "Man", "Patan", "Phaltan", "Satara", "Wai"],
    "Sindhudurg": ["Devgad", "Dodamarg", "Kankavli", "Kudal", "Malvan", "Sawantwadi", "Vaibhavwadi", "Vengurla"],
    "Solapur": ["Akkalkot", "Barshi", "Karmala", "Madha", "Malshiras", "Mangalvedhe", "Mohol", "North Solapur", "Pandharpur", "Sangola", "South Solapur"],
    "Thane": ["Ambarnath", "Bhiwandi", "Kalyan", "Murbad", "Shahapur", "Thane"],
    "Wardha": ["Arvi", "Ashti", "Deoli", "Hinganghat", "Karanja", "Samudrapur", "Seloo", "Wardha"],
    "Washim": ["Karanja", "Malegaon", "Mangrulpir", "Manora", "Risod", "Washim"],
    "Yavatmal": ["Arni", "Babulgaon", "Darwha", "Digras", "Ghatanji", "Kalamb", "Kelapur", "Mahagaon", "Maregaon", "Ner", "Pusad", "Ralegaon", "Umarkhed", "Wani", "Yavatmal", "Zari Jamani"]
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
    district_mr = district.get()
    taluka_mr = taluka.get()
    soil_mr = soil_type.get()
    state_en = STATE_ENGLISH_MAP.get(state_mr, state_mr)
    district_en = DISTRICT_ENGLISH_MAP.get(district_mr, district_mr)
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
- District (Marathi): {district_mr}
- District (English): {district_en}
- Taluka: {taluka_mr}
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
root.geometry("980x670")
root.minsize(920, 620)
root.configure(bg="#f1f8e9")

style = ttk.Style()
style.theme_use("clam")
style.configure("Card.TFrame", background="#ffffff")
style.configure("Title.TLabel", background="#f1f8e9", foreground="#1b5e20", font=("Arial", 22, "bold"))
style.configure("SubTitle.TLabel", background="#f1f8e9", foreground="#33691e", font=("Arial", 11))
style.configure("FormLabel.TLabel", background="#ffffff", foreground="#1b5e20", font=("Arial", 11, "bold"))
style.configure("TButton", font=("Arial", 12, "bold"), padding=8)

# Variables
state = tk.StringVar()
district = tk.StringVar()
taluka = tk.StringVar()
soil_type = tk.StringVar()
n_soil = tk.DoubleVar()
p_soil = tk.DoubleVar()
k_soil = tk.DoubleVar()
temperature = tk.DoubleVar()
humidity = tk.DoubleVar()
ph = tk.DoubleVar()
rainfall = tk.DoubleVar()

district_cb = None
taluka_cb = None


def fetch_talukas_for_district(district_en):
    return MAHARASHTRA_TALUKAS.get(district_en, [])


def update_districts(*_):
    if state.get() == "महाराष्ट्र":
        district_values = [DISTRICT_MARATHI_MAP.get(d, d) for d in MAHARASHTRA_DISTRICTS]
        district_cb["values"] = district_values
        district.set(district_values[0])
        update_talukas()
        return

    district_cb["values"] = ["जिल्हा उपलब्ध नाही"]
    district.set("जिल्हा उपलब्ध नाही")
    taluka_cb["values"] = ["तालुका उपलब्ध नाही"]
    taluka.set("तालुका उपलब्ध नाही")


def update_talukas(*_):
    if state.get() != "महाराष्ट्र":
        taluka_cb["values"] = ["तालुका उपलब्ध नाही"]
        taluka.set("तालुका उपलब्ध नाही")
        return

    district_en = DISTRICT_ENGLISH_MAP.get(district.get())
    if not district_en:
        taluka_cb["values"] = ["तालुका उपलब्ध नाही"]
        taluka.set("तालुका उपलब्ध नाही")
        return

    try:
        talukas = fetch_talukas_for_district(district_en)
    except Exception:
        talukas = []

    if talukas:
        taluka_cb["values"] = talukas
        taluka.set(talukas[0])
        fetch_rainfall(silent=True)
    else:
        taluka_cb["values"] = ["तालुका मिळाला नाही"]
        taluka.set("तालुका मिळाला नाही")


def geocode_taluka(taluka_name, district_en):
    q = quote(f"{taluka_name}, {district_en}, Maharashtra, India")
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
    req = Request(url, headers={"User-Agent": "BE_PROJECT/1.0"})
    with urlopen(req, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not payload:
        raise ValueError("Taluka location not found")
    return float(payload[0]["lat"]), float(payload[0]["lon"])


def get_selected_location_coords():
    if state.get() != "महाराष्ट्र":
        raise ValueError("सध्या auto-fill फक्त महाराष्ट्रासाठी उपलब्ध आहे.")

    district_en = DISTRICT_ENGLISH_MAP.get(district.get())
    if not district_en or taluka.get().endswith("नाही"):
        raise ValueError("कृपया वैध जिल्हा आणि तालुका निवडा.")

    lat, lon = geocode_taluka(taluka.get(), district_en)
    return district_en, lat, lon


def fetch_temperature():
    try:
        _, lat, lon = get_selected_location_coords()
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current=temperature_2m"
        )
        req = Request(url, headers={"User-Agent": "BE_PROJECT/1.0"})
        with urlopen(req, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
        current_temp = payload.get("current", {}).get("temperature_2m")
        if current_temp is None:
            raise ValueError("Temperature not found")
        temperature.set(float(current_temp))
        result_label.config(text=f"{taluka.get()} साठी तापमान भरले: {current_temp}°C", bg="#f1f8e9", fg="#1b5e20")
    except ValueError as e:
        messagebox.showwarning("Location Missing", str(e))
    except (URLError, TimeoutError):
        messagebox.showerror("API Error", "तापमान मिळवताना त्रुटी आली. इंटरनेट/निवड तपासा आणि पुन्हा प्रयत्न करा.")


def fetch_rainfall(silent=False):
    try:
        _, lat, lon = get_selected_location_coords()
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&daily=precipitation_sum&forecast_days=1&timezone=auto"
        )
        req = Request(url, headers={"User-Agent": "BE_PROJECT/1.0"})
        with urlopen(req, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))

        daily = payload.get("daily", {})
        precipitation = daily.get("precipitation_sum", [None])[0]
        if precipitation is None:
            raise ValueError("Rainfall not found")

        rainfall.set(float(precipitation))
        result_label.config(text=f"{taluka.get()} साठी पर्जन्यमान भरले: {precipitation} mm", bg="#f1f8e9", fg="#1b5e20")
    except ValueError as e:
        if not silent:
            messagebox.showwarning("Location Missing", str(e))
    except (URLError, TimeoutError):
        if not silent:
            messagebox.showerror("API Error", "पर्जन्यमान मिळवताना त्रुटी आली. इंटरनेट/निवड तपासा आणि पुन्हा प्रयत्न करा.")

# =========================
# Predict function
# =========================
def predict_crop():
    if model is None:
        messagebox.showerror("Model Error", f"Model load failed:\n{MODEL_LOAD_ERROR}")
        return

    try:
        state_value = STATE_ENGLISH_MAP.get(state.get())
        soil_value = SOIL_ENGLISH_MAP.get(soil_type.get())
        if not state_value or not soil_value or district.get().endswith("उपलब्ध नाही") or taluka.get().endswith("नाही"):
            raise ValueError("State/district/taluka/soil selection missing.")

        data = {
            "STATE": [state_value],
            "SOIL_TYPE": [soil_value],
            "N_SOIL": [float(n_soil.get())],
            "P_SOIL": [float(p_soil.get())],
            "K_SOIL": [float(k_soil.get())],
            "TEMPERATURE": [float(temperature.get())],
            "HUMIDITY": [float(humidity.get())],
            "ph": [float(ph.get())],
            "RAINFALL": [float(rainfall.get())]
        }
    except Exception:
        messagebox.showerror("Error", "कृपया सर्व value योग्य प्रकारे भरा (numbers) आणि राज्य/जिल्हा/तालुका/माती निवडा.")
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
ttk.Label(root, text="🌱 पीक शिफारस प्रणाली", style="Title.TLabel").pack(pady=(18, 4))
ttk.Label(root, text="माती व हवामान आधारित स्मार्ट शिफारस आणि रिपोर्ट जनरेशन", style="SubTitle.TLabel").pack(pady=(0, 14))

frame = ttk.Frame(root, style="Card.TFrame", padding=20)
frame.pack(padx=20, pady=10, fill="x")

# Helper Functions
def add_label(text, row):
    ttk.Label(
        frame,
        text=text,
        style="FormLabel.TLabel"
    ).grid(row=row, column=0, padx=(4, 20), pady=7, sticky="w")

def add_entry(var, row):
    ttk.Entry(frame, textvariable=var, width=24).grid(row=row, column=1, pady=7, sticky="ew")

def add_combo(var, values, row):
    cb = ttk.Combobox(frame, textvariable=var, values=values, width=22, state="readonly")
    cb.grid(row=row, column=1, pady=7, sticky="ew")
    cb.current(0)
    return cb

frame.columnconfigure(1, weight=1)

# Input Fields (Marathi)
add_label("राज्य", 0); state_cb = add_combo(state, state_marathi_list, 0)
add_label("जिल्हा", 1); district_cb = add_combo(district, ["जिल्हा निवडा"], 1)
add_label("तालुका", 2); taluka_cb = add_combo(taluka, ["तालुका निवडा"], 2)
add_label("मातीचा प्रकार", 3); add_combo(soil_type, SOIL_MARATHI_LIST, 3)

add_label("नायट्रोजन (N)", 4); add_entry(n_soil, 4)
add_label("फॉस्फरस (P)", 5); add_entry(p_soil, 5)
add_label("पोटॅशियम (K)", 6); add_entry(k_soil, 6)
add_label("तापमान (°C)", 7); add_entry(temperature, 7)
add_label("आर्द्रता (%)", 8); add_entry(humidity, 8)
add_label("मातीचा pH", 9); add_entry(ph, 9)
add_label("पर्जन्यमान (मिमी)", 10); add_entry(rainfall, 10)

ttk.Button(
    frame,
    text="निवडलेल्या तालुक्याचे तापमान भरा",
    command=fetch_temperature
).grid(row=7, column=2, padx=(10, 0), sticky="ew")

ttk.Button(
    frame,
    text="निवडलेल्या तालुक्याचे पर्जन्यमान भरा",
    command=fetch_rainfall
).grid(row=10, column=2, padx=(10, 0), sticky="ew")

state_cb.bind("<<ComboboxSelected>>", update_districts)
district_cb.bind("<<ComboboxSelected>>", update_talukas)
taluka_cb.bind("<<ComboboxSelected>>", lambda _e: fetch_rainfall(silent=True))
update_districts()

# Button
ttk.Button(
    root,
    text="पीक शिफारस करा + रिपोर्ट तयार करा",
    command=predict_crop
).pack(pady=16)

# Result Label
result_label = tk.Label(
    root,
    text="शिफारसीसाठी वरची माहिती भरा.",
    font=("Arial", 15, "bold"),
    bg="#f1f8e9",
    fg="#1b5e20",
    pady=18
)
result_label.pack(fill="x", padx=14)

if model is None:
    result_label.config(
        text="⚠️ मॉडेल लोड झाले नाही. कृपया model_outputs फोल्डर तपासा.",
        fg="#b71c1c"
    )

root.mainloop()
