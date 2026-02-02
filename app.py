import streamlit as st
from gtts import gTTS
import tempfile
from langdetect import detect
from deep_translator import GoogleTranslator
import pycountry
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Globalize – Language Converter & Speaker",
    layout="wide"
)

st.title("🌍 Globalize – Language Converter & Speaker")

# ---------------- TEXT TO SPEECH ----------------
def read_aloud(text, language="en"):
    tts = gTTS(text=text, lang=language)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# ---------------- WORD CLOUD (NO NLTK) ----------------
def generate_wordcloud(text):
    clean_text = " ".join(text.split())

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white"
    )

    fig, ax = plt.subplots()
    ax.imshow(wc.generate(clean_text))
    ax.axis("off")
    return fig

# ---------------- UI LAYOUT ----------------
col1, col2 = st.columns(2)

with col1:
    paragraph = st.text_area("Enter one paragraph")

with col2:
    languages = sorted([
        lang.name for lang in pycountry.languages
        if hasattr(lang, "alpha_2")
    ])
    target_languages = st.multiselect(
        "Select languages",
        languages
    )

# ---------------- READ ALOUD INPUT ----------------
if st.button("🔊 Read Aloud"):
    if paragraph.strip():
        read_aloud(paragraph)
    else:
        st.warning("Please enter text first")

# ---------------- LANGUAGE DETECTION ----------------
if paragraph.strip():
    try:
        detected_code = detect(paragraph)
        detected_name = pycountry.languages.get(alpha_2=detected_code).name
        st.success(f"Detected language: {detected_name}")
    except:
        detected_code = "en"
        st.warning("Language detection failed, defaulting to English")

# ---------------- TRANSLATE TO ENGLISH ----------------
if paragraph.strip():
    if detected_code != "en":
        translated_en = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(paragraph)

        st.subheader("🔁 Translated to English")
        st.write(translated_en)
    else:
        translated_en = paragraph

    # Word Cloud
    fig = generate_wordcloud(translated_en)
    st.sidebar.subheader("☁ Word Cloud")
    st.sidebar.pyplot(fig)

# ---------------- MULTI LANGUAGE TRANSLATE + SPEAK ----------------
if st.button("🌐 Translate and Speak"):
    if not paragraph.strip():
        st.warning("Please enter text first")
    else:
        for lang in target_languages:
            try:
                code = pycountry.languages.lookup(lang).alpha_2
                translated = GoogleTranslator(
                    source="auto",
                    target=code
                ).translate(paragraph)

                st.subheader(lang)
                st.write(translated)

                # Speak translated text
                read_aloud(translated, code)

            except Exception as e:
                st.error(f"Failed for {lang}")



