import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib.pyplot as plt
import string

st.title("🧠 Web Words Frequency Counter (MapReduce)")

# Функції

def get_clean_text_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        st.error(f"❌ Error fetching URL: {e}")
        return ""
    
    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup(['script', 'style']):
        tag.decompose()
    text = soup.get_text(separator=' ')
    return ' '.join(text.split())

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word.lower(), 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text, search_words=None):
    text = remove_punctuation(text)
    words = text.split()

    if search_words:
        words = [word for word in words if word.lower() in search_words]

    mapped = list(map(map_function, words))
    shuffled = shuffle_function(mapped)
    reduced = [reduce_function(item) for item in shuffled]
    return dict(reduced)

def plot_words(freq_dict, top_n=15):
    sorted_words = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]
    if not sorted_words:
        st.warning("No words to display.")
        return

    words, counts = zip(*sorted_words)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(words, counts, color='skyblue')
    ax.set_xlabel("Frequency")
    ax.set_title(f"Top {top_n} Words")
    ax.invert_yaxis()
    st.pyplot(fig)

# Інтерфейс

url = st.text_input("🔗 Введіть URL веб-сторінки", "https://finance.yahoo.com/news/wall-street-plays-long-game-190000469.html")

exclude_words_input = st.text_area("✂️ Введіть стоп-слова для виключення (через кому)", "the, and, of, a, to, in")
exclude_words = set(word.strip().lower() for word in exclude_words_input.split(','))

top_n = st.slider("📊 Кількість топ-слів для відображення", 5, 50, 15)

if st.button("🔍 Аналізувати"):
    with st.spinner("Завантаження..."):
        raw_text = get_clean_text_from_url(url)
        if raw_text:
            result = map_reduce(raw_text)
            filtered = {word: count for word, count in result.items() if word not in exclude_words}
            st.success("✅ Готово!")
            st.write("📈 Результат підрахунку:", filtered)
            plot_words(filtered, top_n=top_n)
