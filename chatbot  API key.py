import tkinter as tk

from tkinter import scrolledtext, messagebox
from google import genai
import os

# ==============================
# GEMINI CONFIG
# ==============================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = "gemini-2.5-flash"

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# ==============================
# GEMINI FARMER RESPONSE
# ==============================
def farmer_response(user_message: str) -> str:
    if not GEMINI_API_KEY or client is None:
        return "⚠️ Gemini API key missing. Set GEMINI_API_KEY environment variable and restart chatbot."

    try:
        detail = "short and simple" if var_short.get() else "detailed but easy to understand"
        reply_lang = "Marathi" if var_marathi.get() else "English"

        prompt = f"""
You are a Farmer Agriculture Assistant for India.

You help farmers with:
- soil improvement and soil health
- crop planning and seasonal guidance
- irrigation methods (drip, sprinkler, schedule)
- fertilizers (NPK concepts, organic vs chemical) — NO exact dosage
- pest prevention using IPM (integrated pest management)
- disease prevention (general) — NO pesticide dosage/brands
- post-harvest storage and market tips

STRICT RULES:
- Do NOT give pesticide/chemical exact dosage or brand recommendations.
- Do NOT guarantee results.
- If farmer has severe crop damage, advise contacting local Krishi Sevak / Agriculture officer.
- Keep advice practical & actionable.

Answer style: {detail}
Reply language: {reply_lang}

User question:
{user_message}
"""
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        if getattr(response, "text", None):
            return response.text.strip()

        return "⚠️ I received an empty response from Gemini. Please try again."

    except Exception as e:
        return f"⚠️ Unable to connect to Farmer AI service right now: {e}"

# ==============================
# SEND MESSAGE
# ==============================
def send_message():
    user_text = entry_msg.get().strip()
    if not user_text:
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {user_text}\n", "user")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

    entry_msg.delete(0, tk.END)

    reply = farmer_response(user_text)

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"Farmer AI: {reply}\n\n", "bot")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

def clear_chat():
    chat_area.config(state=tk.NORMAL)
    chat_area.delete("1.0", tk.END)
    chat_area.config(state=tk.DISABLED)
    welcome_message()

# ==============================
# MAIN WINDOW
# ==============================
root = tk.Tk()
root.title("Farmer Assistance Chatbot (Gemini)")
root.geometry("900x600")
root.configure(bg="white")

# ==============================
# HEADER
# ==============================
header = tk.Label(
    root,
    text="Farmer Assistance Chatbot",
    font=("Segoe UI", 20, "bold"),
    bg="white",
    fg="#16a34a"
)
header.pack(pady=10)

sub_header = tk.Label(
    root,
    text="Soil • Crop Planning • Irrigation • Organic Farming • Pest Prevention (IPM)",
    font=("Segoe UI", 11),
    bg="white",
    fg="#475569"
)
sub_header.pack()

# ==============================
# CHAT AREA
# ==============================
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    bg="#f8fafc",
    fg="#0f172a",
    state=tk.DISABLED
)
chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

chat_area.tag_config("user", foreground="#1d4ed8", font=("Segoe UI", 11, "bold"))
chat_area.tag_config("bot", foreground="#0f172a", font=("Segoe UI", 11))

# ==============================
# OPTIONS
# ==============================
options_frame = tk.Frame(root, bg="white")
options_frame.pack(fill=tk.X, padx=15)

var_short = tk.BooleanVar(value=True)
var_marathi = tk.BooleanVar(value=True)

tk.Checkbutton(
    options_frame,
    text="Short answer",
    variable=var_short,
    bg="white",
    fg="#0f172a",
    activebackground="white"
).pack(side=tk.LEFT)

tk.Checkbutton(
    options_frame,
    text="Reply in Marathi",
    variable=var_marathi,
    bg="white",
    fg="#0f172a",
    activebackground="white"
).pack(side=tk.LEFT, padx=(12, 0))

tk.Button(
    options_frame,
    text="Clear Chat",
    command=clear_chat,
    bg="#ef4444",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=12
).pack(side=tk.RIGHT)

# ==============================
# INPUT AREA
# ==============================
input_frame = tk.Frame(root, bg="white")
input_frame.pack(fill=tk.X, padx=15, pady=15)

entry_msg = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    bg="white",
    fg="#0f172a",
    relief=tk.SOLID
)
entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
entry_msg.focus()

send_btn = tk.Button(
    input_frame,
    text="Send",
    bg="#16a34a",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    padx=25,
    command=send_message
)
send_btn.pack(side=tk.RIGHT, padx=(10, 0))

root.bind("<Return>", lambda e: send_message())

# ==============================
# WELCOME MESSAGE
# ==============================
def welcome_message():
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(
        tk.END,
        "Farmer AI: नमस्कार \n"
        "मी तुमचा Farmer Assistance Chatbot आहे.\n\n"
        "मी मदत करू शकतो:\n"
        "- माती सुधारणा / Soil health\n"
        "- कोणते पीक घ्यावे (हंगामानुसार माहिती)\n"
        "- सिंचन मार्गदर्शन (ड्रिप/स्प्रिंकलर)\n"
        "- सेंद्रिय शेती आणि खत व्यवस्थापन (general)\n"
        "- किड/रोग प्रतिबंध (IPM - general)\n"
        "- काढणी नंतर साठवणूक व बाजार टिप्स\n\n"
        "⚠️ मी pesticide/chemical ची exact dosage किंवा brand सांगत नाही.\n"
        "मोठे नुकसान/रोग असल्यास स्थानिक कृषी अधिकारी/कृषी सेवक यांना भेटा.\n\n",
        "bot"
    )
    chat_area.config(state=tk.DISABLED)

welcome_message()

# ==============================
# RUN APP
# ==============================
root.mainloop()

