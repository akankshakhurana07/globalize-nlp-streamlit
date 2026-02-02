# 🌍 Globalize – Language Converter & Speaker  

**Globalize** is a production-ready NLP web application that detects the language of user-provided text, translates it into multiple global languages, and converts translated text into natural-sounding speech — all through a clean, interactive Streamlit interface.

🔗 **Live Application:**  
https://globalize-nlp-app-wfnextsglmgmqbcxldzmrj.streamlit.app/

---

## 📌 Project Overview

In today’s globalized world, language should never be a barrier.  
**Globalize** bridges communication gaps by combining **Natural Language Processing (NLP)**, **machine translation**, and **text-to-speech (TTS)** into a single, easy-to-use web application.

The app is fully deployed on **Streamlit Cloud Community** and optimized for browser-based usage (no system-level dependencies).

---

## ✨ Key Features

- 🌐 **Automatic Language Detection** – Detects the source language of the input text  
- 🔁 **Multi-Language Translation** – Translate text into multiple selected languages  
- 🔊 **Text-to-Speech (TTS)** – Browser-based audio playback for translated text  
- ☁️ **Word Cloud Visualization** – Highlights important terms from English translation  
- 🖥️ **Clean & Interactive UI** – Built with Streamlit for simplicity and speed  

---

## 🧠 How It Works

1. User enters a paragraph of text  
2. Application automatically detects the input language  
3. Text is translated into English (universal processing language)  
4. A word cloud is generated from the English translation  
5. Text is translated into selected target languages  
6. Each translation is spoken aloud using browser audio  

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Frontend | Streamlit |
| Language Detection | langdetect |
| Translation Engine | deep-translator |
| Text-to-Speech | Google Text-to-Speech (gTTS) |
| Language Metadata | pycountry |
| Visualization | wordcloud, matplotlib |
| Deployment | Streamlit Cloud Community |

---

## 📂 Project Structure

globalize-nlp-streamlit/
│
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md # Project documentation




