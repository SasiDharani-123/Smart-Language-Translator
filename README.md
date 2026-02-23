# Smart-Language-Translator

A modern AI-powered language translator built using **Streamlit** and **Google Gemini API** with Text-to-Speech support.

## 🚀 Features

- 🌐 Translate between multiple languages
- 🔄 Swap source and target languages
- 🗑 Clear input & output instantly
- 📊 Word & character counter
- 🔊 Text-to-Speech for translated text
- 📚 Translation history (sidebar)
- 🌙 Dark UI with Sky Blue theme
- ⚡ Powered by Google Gemini AI

## 🛠 Tech Stack

- Python
- Streamlit
- Google Generative AI (Gemini API)
- gTTS (Google Text-to-Speech)
- python-dotenv

## 📦 Installation & Setup

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```
If you don't have requirements.txt, install manually:

```bash
pip install streamlit google-generativeai python-dotenv gtts
```

### 4️⃣ Setup Environment Variables

Create a file named:

```
.env
```

Inside it, add your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

## ▶️ Run the Application

```bash
streamlit run translang.py
```
---

## 📌 Future Improvements

- 🌍 Auto language detection
- 📋 Copy to clipboard button
- 📥 Export as TXT
- 🎤 Voice input
- ☁ Deploy on Streamlit Cloud

