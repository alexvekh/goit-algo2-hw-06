# Web Words Frequency Counter with MapReduce
This project allows you to download text from any web page, count word frequencies using the MapReduce concept, exclude unnecessary words, and visualize the most frequent ones in a chart.

[![Streamlit App](https://img.shields.io/badge/Live%20App-Open%20Now-brightgreen?style=for-the-badge)](https://webwords.streamlit.app//)

## 🧠 How It Works?
 -Downloads an HTML page from a given URL.
- Cleans the text by removing HTML tags, scripts, styles, and punctuation.
- Counts the frequency of each word using the MapReduce approach:
  - map_function → creates pairs (word, 1)
  - shuffle_function → groups all identical words
  - reduce_function → calculates the total count for each word
- Allows you to specify a list of desired words
- Allows you to exclude a list of stop-words or articles (e.g., "the", "and", "of"...)
- Builds a horizontal bar chart for the top 15 words (Visualization)

## 🛠️ Requirements
Python 3.x

Install dependencies:

        python -m venv venv
        venv\Scripts\activate       

        pip install requests beautifulsoup4 matplotlib

        python web-words.py

## You can modify in the code:
- Web page URL:

        url = "https://finance.yahoo.com/news/wall-street-plays-long-game-190000469.html"

- List of target words:

        search_words = ["inflation", "stocks", "recession"]

- Stop-words to exclude:

        exclude_words = {'the', 'a', 'an', 'of', 'and'}

## 📈 Sample Output
- Word count result: {'inflation': 12, 'stocks': 10, 'growth': 8}
- A chart with the most frequent words will also be displayed in a new window.

