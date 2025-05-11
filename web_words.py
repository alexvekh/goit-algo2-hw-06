import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def get_clean_text_from_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Видалити скрипти та стилі
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Витягнути текст
    text = soup.get_text(separator=' ')
    
    # Очистити зайві пробіли
    clean_text = ' '.join(text.split())
    return clean_text

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None


# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


# Виконання MapReduce
def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Маппінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# Функція побудови графіка
def visualize_top_words(result, top_n=20):
    # Visualize the top 10 words and their frequencies using a horizontal bar chart ((dict), top_n=10 ) 

    # Sort the word frequencies dictionary by frequency in descending order and select the top N words
    sorted_words = sorted(result.items(), key=lambda item: item[1], reverse=True)[:top_n]

    # Separate the words and their frequencies for plotting
    words, frequencies = zip(*sorted_words)

    # Create a horizontal bar chart
    plt.figure(figsize=(10, 8))
    plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest frequency word at the top
    plt.show()


if __name__ == "__main__":
    # Вхідний текст для обробки
    # url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    url = "https://finance.yahoo.com/news/wall-street-plays-long-game-190000469.html"  
    # text = get_text(url)
    text = get_clean_text_from_url(url)

    if text:
        # Виконання MapReduce на вхідному тексті
        # search_words = ["war", "peace", "love"]
        search_words = []
        result = map_reduce(text, search_words)
        exclude_words = {'The', 'the', 'a', 'an', 'of', 'to', 'and', 'in', 'it', 'that', 'not', 'as', 'is', 'at', 'for', 'but', 'on', 'or', 'by', 'from', "News", "US"}  # Множина слів, які хочеш виключити
        filtered_result = {word: count for word, count in result.items() if word not in exclude_words}

        sorted_result = dict(sorted(filtered_result.items(), key=lambda item: item[1], reverse=False))



        print("Результат підрахунку слів:", sorted_result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")

    visualize_top_words(sorted_result)