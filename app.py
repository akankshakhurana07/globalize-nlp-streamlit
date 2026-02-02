import streamlit as st
from gtts import gTTS
import tempfile
from langdetect import detect
from deep_translator import GoogleTranslator
import pycountry
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize

# ------------------ NLTK SETUP (cloud safe) ------------------
@st.cache_resource
def download_nltk():
    nltk.download("punkt")
    nltk.download("words")

download_nltk()

# ------------------ TEXT TO SPEECH ------------------
def read_aloud(text, language="en"):
    tts = gTTS(text=text, lang=language)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# ------------------ WORD CLOUD ------------------
def generate_wordcloud(text):
    english_words = set(nltk.corpus.words.words())
    words = word_tokenize(text)
    filtered = [w for w in words if w.lower() in english_words]
    clean_text = " ".join(filtered)

    wc = WordCloud(width=800, height=400, background_color="white")
    fig, ax = plt.subplots()
    ax.imshow(wc.generate(clean_text))
    ax.axis("off")
    return fig

# ------------------ UI ------------------
st.set_page_config(page_title="Globalize", layout="wide")
st.title("🌍 Globalize – Language Converter & Speaker")

col1, col2 = st.columns(2)

with col1:
    paragraph = st.text_area("Enter one paragraph")

with col2:
    languages = sorted([l.name for l in pycountry.languages if hasattr(l, "alpha_2")])
    targets = st.multiselect("Select languages", languages)

# ------------------ READ ALOUD ------------------
if st.button("Read Aloud"):
    if paragraph.strip():
        read_aloud(paragraph)

# ------------------ LANGUAGE DETECT ------------------
if paragraph.strip():
    try:
        detected = detect(paragraph)
        lang_name = pycountry.languages.get(alpha_2=detected).name
        st.success(f"Detected language: {lang_name}")
    except:
        detected = "en"

# ------------------ TRANSLATE TO ENGLISH ------------------
if paragraph.strip():
    if detected != "en":
        translated_en = GoogleTranslator(source="auto", target="en").translate(paragraph)
        st.subheader("Translated to English")
        st.write(translated_en)
    else:
        translated_en = paragraph

    # word cloud
    fig = generate_wordcloud(translated_en)
    st.sidebar.subheader("Word Cloud")
    st.sidebar.pyplot(fig)

# ------------------ MULTI TRANSLATE + SPEAK ------------------
if st.button("Translate and Speak"):
    for lang in targets:
        try:
            code = pycountry.languages.lookup(lang).alpha_2
            translated = GoogleTranslator(source="auto", target=code).translate(paragraph)
            st.subheader(lang)
            st.write(translated)
            read_aloud(translated, code)
        except:
            st.error(f"Failed for {lang}")


