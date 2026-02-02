import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
import pycountry
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize

# -------------------- NLTK SETUP --------------------
@st.cache_resource
def download_nltk():
    nltk.download("punkt")
    nltk.download("words")

download_nltk()

# -------------------- FUNCTIONS --------------------
def generate_wordcloud(text):
    english_words = set(nltk.corpus.words.words())
    words = word_tokenize(text)
    filtered_words = [w for w in words if w.lower() in english_words]
    clean_text = " ".join(filtered_words)

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(clean_text)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig

def get_lang_code(lang_name):
    try:
        return pycountry.languages.lookup(lang_name).alpha_2
    except:
        return None

# -------------------- UI --------------------
st.set_page_config(page_title="Globalize", layout="wide")
st.title("🌍 Globalize – NLP Translation Studio")

col1, col2 = st.columns(2)

with col1:
    paragraph = st.text_area("Enter one paragraph:")

with col2:
    all_languages = sorted([lang.name for lang in pycountry.languages if hasattr(lang, "alpha_2")])
    target_languages = st.multiselect(
        "Select target languages:",
        all_languages
    )

# -------------------- LANGUAGE DETECTION --------------------
if paragraph.strip():
    try:
        detected_lang = detect(paragraph)
        detected_name = pycountry.languages.get(alpha_2=detected_lang).name
        st.success(f"Detected language: {detected_name}")
    except:
        detected_lang = "en"
        st.warning("Could not detect language, defaulting to English")

# -------------------- TRANSLATE TO ENGLISH --------------------
if paragraph.strip():
    if detected_lang != "en":
        translated_en = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(paragraph)

        st.subheader("🔁 Translated to English")
        st.write(translated_en)
    else:
        translated_en = paragraph

    # -------------------- WORD CLOUD --------------------
    try:
        fig = generate_wordcloud(translated_en)
        st.sidebar.subheader("☁ Word Cloud")
        st.sidebar.pyplot(fig)
    except Exception as e:
        st.sidebar.error(f"WordCloud error: {e}")

# -------------------- MULTI-LANGUAGE TRANSLATION --------------------
if st.button("Translate"):
    if not paragraph.strip():
        st.warning("Please enter text first")
    else:
        for lang in target_languages:
            code = get_lang_code(lang)
            if not code:
                continue

            try:
                translated_text = GoogleTranslator(
                    source="auto",
                    target=code
                ).translate(paragraph)

                st.subheader(f"🌐 {lang}")
                st.write(translated_text)

            except Exception as e:
                st.error(f"Failed for {lang}: {e}")

