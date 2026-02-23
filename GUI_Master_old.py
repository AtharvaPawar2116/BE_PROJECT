import tkinter as tk
from tkinter import ttk, LEFT, END, messagebox
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import time
import os
import json
from datetime import datetime
import threading

# Note: Ensure CNNModel.py is in the same directory
# import CNNModel 

# =========================================================
# COLORS & THEME
# =========================================================
BG_COLOR = "#f4f7f6"
SIDEBAR_COLOR = "#2c3e50"
ACCENT_COLOR = "#27ae60"
TEXT_COLOR = "#2c3e50"
CARD_COLOR = "#ffffff"

class CropPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(background=BG_COLOR)
        self.w, self.h = root.winfo_screenwidth(), root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.title("Soil Based - Crop Prediction System")

        self.fn = ""
        self.model_path = "dataset/soil_model_cnn.h5"
        self.class_index_path = "dataset/class_indices.json"
        self.non_soil_threshold = 65.0
        self.slot_width = 340
        self.slot_height = 260
        
        # --- UI SETUP ---
        self.setup_sidebar()
        self.setup_main_area()
        
    # =========================================================
    # UI COMPONENTS
    # =========================================================
    def setup_sidebar(self):
        sidebar = tk.Frame(self.root, bg=SIDEBAR_COLOR, width=300, height=self.h)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        title = tk.Label(sidebar, text="AGRO PREDICT", font=("Arial", 20, "bold"), 
                         bg=SIDEBAR_COLOR, fg="white", pady=30)
        title.pack()

        btn_style = {"font": ("Arial", 12, "bold"), "bg": "#34495e", "fg": "white", 
                     "activebackground": ACCENT_COLOR, "bd": 0, "pady": 12, "cursor": "hand2"}

        tk.Button(sidebar, text="Select Image", command=self.openimage, **btn_style).pack(fill="x", padx=20, pady=5)
        tk.Button(sidebar, text="Pre-Process", command=self.convert_grey, **btn_style).pack(fill="x", padx=20, pady=5)
        tk.Button(sidebar, text="Train CNN Model", command=self.train_cnn_model, **btn_style).pack(fill="x", padx=20, pady=5)
        tk.Button(sidebar, text="CNN Prediction", command=self.test_model, **btn_style).pack(fill="x", padx=20, pady=5)
        tk.Button(sidebar, text="SVM Prediction", command=self.svm_predication, **btn_style).pack(fill="x", padx=20, pady=5)
        tk.Button(sidebar, text="AI Chatbot", command=self.chatbot, **btn_style).pack(fill="x", padx=20, pady=5)
        
        tk.Button(sidebar, text="Exit", command=self.root.destroy, font=("Arial", 12), 
                  bg="#e74c3c", fg="white", bd=0, pady=10).pack(side="bottom", fill="x", padx=20, pady=30)

    def setup_main_area(self):
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=30, pady=20)

        # Header
        header = tk.Label(self.main_frame, text="Crop Prediction Dashboard", font=("Arial", 26, "bold"), 
                          bg=BG_COLOR, fg=TEXT_COLOR)
        header.pack(anchor="nw", pady=(0, 20))

        # Image Display Container
        self.img_container = tk.Frame(self.main_frame, bg=CARD_COLOR, relief="groove", bd=1)
        self.img_container.pack(fill="x")

        self.lbl_orig = self.create_img_slot(self.img_container, "Input Soil Image", 0)
        self.lbl_gray = self.create_img_slot(self.img_container, "Grayscale", 1)
        self.lbl_bin = self.create_img_slot(self.img_container, "Binary/Otsu", 2)

        # Status Bar
        self.status_label = tk.Label(self.main_frame, text="Ready: Please upload a soil image", 
                                     font=('Arial', 13, 'italic'), bg="#f1c40f", fg="black", height=2)
        self.status_label.pack(fill="x", pady=20)

        # Recommendation Display Area
        self.res_frame = tk.Frame(self.main_frame, bg=SIDEBAR_COLOR, pady=15, padx=15)
        self.res_frame.pack(fill="both", expand=True)

        self.crop_label = tk.Label(self.res_frame, text="Recommendations will appear here...", 
                                   font=("Arial", 13), bg=SIDEBAR_COLOR, fg="white", 
                                   justify="left", anchor="nw", wraplength=800)
        self.crop_label.pack(fill="both", expand=True)

    def create_img_slot(self, parent, text, col):
        frame = tk.Frame(parent, bg="white", padx=10, pady=10)
        frame.grid(row=0, column=col)
        tk.Label(frame, text=text, font=("Arial", 11, "bold"), bg="white", fg="grey").pack(pady=(0, 8))

        canvas = tk.Canvas(
            frame,
            bg="#ecf0f1",
            width=self.slot_width,
            height=self.slot_height,
            relief="ridge",
            bd=1,
            highlightthickness=0
        )
        canvas.pack()
        return canvas

    def _fit_image_to_slot(self, pil_img):
        img = pil_img.copy()
        img.thumbnail((self.slot_width, self.slot_height), Image.LANCZOS)

        fitted = Image.new("RGB", (self.slot_width, self.slot_height), "#ecf0f1")
        x = (self.slot_width - img.width) // 2
        y = (self.slot_height - img.height) // 2
        fitted.paste(img, (x, y))
        return fitted

    def _show_image_on_slot(self, slot_canvas, pil_img):
        fitted = self._fit_image_to_slot(pil_img)
        imgtk = ImageTk.PhotoImage(fitted)
        slot_canvas.delete("all")
        slot_canvas.create_image(0, 0, anchor="nw", image=imgtk)
        slot_canvas.image = imgtk

    # =========================================================
    # YOUR ORIGINAL LOGIC (Unchanged, just method-wrapped)
    # =========================================================
    SOIL_RECO = {
        0: {
            "soil_mar": "काळी माती", "soil_en": "Black Soil", "temp": "25°C ते 32°C",
            "crops": ["सोयाबीन", "ज्वारी", "बाजरी", "एरंड"],
            "soil_details": "काळी माती (Black soil) मध्ये चिकणमातीचे प्रमाण जास्त असते...",
            "steps": ["माती परीक्षण करा", "निचरा चांगला ठेवा"],
            "crop_notes": {"सोयाबीन": "पाणी साचू देऊ नका."}
        },
        1: {
            "soil_mar": "गाळाची माती", "soil_en": "Alluvial Soil", "temp": "20°C ते 27°C",
            "crops": ["भात", "गहू", "ऊस", "कापूस"],
            "soil_details": "गाळाची माती साधारणतः सुपीक असते...",
            "steps": ["पिकानुसार योग्य लागवड पद्धत निवडा"],
            "crop_notes": {"भात": "पाण्याचे योग्य नियोजन करा."}
        },
        2: {"soil_mar": "लेटराइट माती", "soil_en": "Laterite Soil", "temp": "14°C ते 36°C", "crops": ["चहा", "कॉफी", "नारळ"], "soil_details": "आम्लीय (acidic) असू शकते...", "steps": ["चुना (liming) करा"], "crop_notes": {}},
        3: {"soil_mar": "पिवळी माती", "soil_en": "Yellow Soil", "temp": "15°C ते 20°C", "crops": ["बटाटा", "डाळी"], "soil_details": "सेंद्रिय पदार्थ कमी असू शकतो...", "steps": ["नत्रयुक्त खतांची विभागणी"], "crop_notes": {}},
        4: {"soil_mar": "वाळूची माती", "soil_en": "Sandy Soil", "temp": "10°C ते 19°C", "crops": ["कलिंगड", "टोमॅटो"], "soil_details": "निचरा जलद होतो...", "steps": ["मल्चिंग करा"], "crop_notes": {}}
    }

    def build_report_text(self, image_path, class_id, confidence_pct):
        rec = self.SOIL_RECO.get(class_id, None)
        if rec is None: return "No recommendation found."
        crops_str = ", ".join(rec["crops"])
        steps_str = "\n".join([f"{i+1}. {s}" for i, s in enumerate(rec["steps"])])
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return f"Report Generated: {now}\nSoil: {rec['soil_en']}\nConfidence: {confidence_pct:.2f}%\nCrops: {crops_str}\nSteps:\n{steps_str}"

    def write_report_to_file(self, report_text, image_path):
        try:
            os.makedirs("reports", exist_ok=True)
            base = os.path.splitext(os.path.basename(image_path))[0]
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join("reports", f"{base}_report_{ts}.txt")
            with open(report_path, "w", encoding="utf-8") as f: f.write(report_text)
            return report_path
        except: return None

    def update_label(self, str_T):
        self.status_label.config(text=str_T)

    def _show_non_soil_warning(self, confidence=None):
        conf_text = f" (confidence: {confidence:.2f}%)" if confidence is not None else ""
        self.crop_label.config(
            text=(
                "⚠️ Non-soil image detected.\n"
                "The selected image appears to be a human/non-soil object.\n"
                "Please upload a clear soil image for crop recommendations."
            )
        )
        self.update_label(f"Prediction blocked: Non-soil image detected{conf_text}")

    def _load_class_mapping(self):
        """Return index->class_name mapping saved during training."""
        if not os.path.exists(self.class_index_path):
            return {}
        try:
            with open(self.class_index_path, "r", encoding="utf-8") as fp:
                raw = json.load(fp)
            return {int(v): k for k, v in raw.items()}
        except Exception:
            return {}

    def _is_non_soil_class(self, class_name):
        if not class_name:
            return False
        key = class_name.lower()
        return (
            "non_soil" in key
            or "nonsoil" in key
            or "human" in key
            or "person" in key
        )

    def show_crop_info(self, class_id):
        rec = self.SOIL_RECO.get(class_id, None)
        if rec:
            self.crop_label.config(text=f"पिकाची शिफारस:\nतापमान: {rec['temp']}\nपीक यादी: {', '.join(rec['crops'])}\n\nमाहिती: {rec['soil_details']}")

    def openimage(self):
        fileName = askopenfilename(initialdir='D:/', title='Select image', filetypes=[("all files", "*.*")])
        if fileName:
            self.fn = fileName
            img = Image.open(self.fn).convert("RGB")
            self._show_image_on_slot(self.lbl_orig, img)
            self.crop_label.config(text="Image loaded. You can preprocess, train model, or run prediction.")
            self.update_label("Image loaded successfully")

    def convert_grey(self):
        if not self.fn:
            self.update_label("Please select image first")
            return
        img_cv = cv2.imread(self.fn)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        gray_disp = cv2.resize(gray, (self.slot_width, self.slot_height))

        gray_img = Image.fromarray(gray_disp).convert("RGB")
        self._show_image_on_slot(self.lbl_gray, gray_img)

        _, thresh = cv2.threshold(gray_disp, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        thresh_img = Image.fromarray(thresh).convert("RGB")
        self._show_image_on_slot(self.lbl_bin, thresh_img)
        self.update_label("Pre-processing completed")

    def _run_training_job(self):
        try:
            from CNNModel import main as train_main
            msg = train_main()
            self.update_label("Training completed")
            messagebox.showinfo("Training Done", msg)
        except Exception as e:
            self.update_label("Training failed")
            messagebox.showerror("Training Error", str(e))

    def train_cnn_model(self):
        self.update_label("Training started... this may take time")
        self.crop_label.config(
            text=(
                "Training in progress...\n"
                "Tip: Keep dataset folders organized as train/test with class subfolders.\n"
                "Include a `non_soil_human` class to avoid wrong soil prediction on human images."
            )
        )
        threading.Thread(target=self._run_training_job, daemon=True).start()

    def test_model(self):
        if self.fn == "":
            self.update_label("Please Select Image First!")
            return
        
        from tensorflow.keras.models import load_model
        try:
            model_file = self.model_path if os.path.exists(self.model_path) else "soil_model_cnn.h5"
            model = load_model(model_file, compile=False)
            img = Image.open(self.fn).resize((100, 100))
            img_arr = np.array(img).reshape(1, 100, 100, 3).astype('float32') / 255.0
            prediction = model.predict(img_arr)
            class_id = int(np.argmax(prediction))
            conf = float(np.max(prediction)) * 100.0
            class_map = self._load_class_mapping()
            class_name = class_map.get(class_id, "")

            # Block prediction for explicit non-soil/human class labels.
            if self._is_non_soil_class(class_name):
                self._show_non_soil_warning(confidence=conf)
                return

            # Backward-safe fallback for legacy models without class mapping.
            if class_id not in self.SOIL_RECO or conf < self.non_soil_threshold:
                self._show_non_soil_warning(confidence=conf)
                return

            self.show_crop_info(class_id)
            soil_name = self.SOIL_RECO[class_id]['soil_mar']
            extra = f" | Class: {class_name}" if class_name else ""
            self.update_label(f"Soil Identified: {soil_name} ({conf:.2f}%){extra}")
            
            report = self.build_report_text(self.fn, class_id, conf)
            path = self.write_report_to_file(report, self.fn)
            if path: messagebox.showinfo("Done", f"Report saved at {path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def svm_predication(self):
        from subprocess import call
        call(["python", "check_predict.py"])
        
    def chatbot(self):
        from subprocess import call
        call(["python", "chatbot API key.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = CropPredictionApp(root)
    root.mainloop()
