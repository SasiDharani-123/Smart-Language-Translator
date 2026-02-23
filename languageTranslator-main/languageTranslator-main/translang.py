from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from gtts import gTTS

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Smart AI Translator",
    page_icon="🌍",
    layout="centered"
)

# ---------------------------------
# DARK THEME COLORS
# ---------------------------------
background_color = "#0f172a"
text_color = "#ffffff"
card_color = "#1e293b"
primary_color = "#38bdf8"

# ---------------------------------
# CUSTOM CSS
# ---------------------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {background_color};
    color: {text_color};
}}

.main-title {{
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 30px;
    color: {primary_color};
}}

.stTextArea textarea {{
    border-radius: 12px;
    padding: 12px;
    background-color: {card_color};
    color: white;
}}

.stButton>button {{
    border-radius: 12px;
    height: 45px;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    background-color: {primary_color};
    color: black;
    border: none;
}}

.stButton>button:hover {{
    background-color: #0ea5e9;
    color: white;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌍 Smart AI Language Translator</div>', unsafe_allow_html=True)

# ---------------------------------
# LOAD API KEY
# ---------------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found in .env file")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-flash-latest")

# ---------------------------------
# LANGUAGES
# ---------------------------------
languages = [
    "English", "Spanish", "French", "German",
    "Chinese", "Hindi", "Telugu",
    "Tamil", "Kannada", "Malayalam"
]

# ---------------------------------
# SESSION STATE INIT
# ---------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "English"

if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Spanish"

# ---------------------------------
# CALLBACK FUNCTIONS
# ---------------------------------
def clear_all():
    st.session_state.input_text = ""
    st.session_state.translated_text = ""

def swap_languages():
    st.session_state.source_lang, st.session_state.target_lang = (
        st.session_state.target_lang,
        st.session_state.source_lang
    )

# ---------------------------------
# INPUT
# ---------------------------------
st.text_area(
    "📝 Enter text to translate:",
    key="input_text"
)

st.caption(
    f"Input Words: {len(st.session_state.input_text.split())} | "
    f"Characters: {len(st.session_state.input_text)}"
)

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "🌐 Source Language:",
        languages,
        key="source_lang"
    )

with col2:
    st.selectbox(
        "🎯 Target Language:",
        languages,
        key="target_lang"
    )

# ---------------------------------
# BUTTONS
# ---------------------------------
col3, col4, col5 = st.columns(3)

with col3:
    st.button("🔁 Translate")

with col4:
    st.button("🗑 Clear", on_click=clear_all)

with col5:
    st.button("🔄 Swap", on_click=swap_languages)

# ---------------------------------
# TRANSLATE FUNCTION
# ---------------------------------
def translate_text(text, source, target):
    prompt = f"Translate from {source} to {target}. Only return the translated text:\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# ---------------------------------
# TRANSLATE ACTION
# ---------------------------------
if st.button("Do Translation", key="hidden_translate", help="internal"):
    pass  # dummy button to avoid rerun issue

if st.session_state.input_text and st.button:
    pass

if st.session_state.get("input_text") and st.session_state.get("source_lang") != st.session_state.get("target_lang"):
    pass

# Real translate logic
if st.session_state.get("input_text") and st.session_state.get("source_lang") != st.session_state.get("target_lang"):
    if st.session_state.get("translated_text") == "":
        try:
            translated = translate_text(
                st.session_state.input_text,
                st.session_state.source_lang,
                st.session_state.target_lang
            )
            st.session_state.translated_text = translated

            st.session_state.history.append({
                "original": st.session_state.input_text,
                "translated": translated
            })

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ---------------------------------
# SHOW RESULT
# ---------------------------------
if st.session_state.translated_text:
    st.subheader("📘 Translated Text:")

    st.text_area(
        "Result:",
        value=st.session_state.translated_text,
        height=150
    )

    st.caption(
        f"Output Words: {len(st.session_state.translated_text.split())} | "
        f"Characters: {len(st.session_state.translated_text)}"
    )

    # Text to Speech
    tts = gTTS(st.session_state.translated_text)
    tts.save("audio.mp3")
    st.audio("audio.mp3")

# ---------------------------------
# SIDEBAR HISTORY
# ---------------------------------
st.sidebar.title("📚 Translation History")

for item in reversed(st.session_state.history):
    st.sidebar.write("🔹", item["original"])
    st.sidebar.write("➡", item["translated"])
    st.sidebar.markdown("---")