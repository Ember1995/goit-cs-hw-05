import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import requests
from heapq import nlargest
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка статусу відповіді
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None


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


def map_reduce(text):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Фільтрація слів довжиною менше 5-ти букв
    words = [word for word in words if len(word) >= 5]

    # Крок 1: Mapping
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Reduction
    with ThreadPoolExecutor() as executor:
        reduced_values = dict(executor.map(reduce_function, shuffled_values))
    return reduced_values


def visualize_top_words(word_frequencies):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequencies)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100011h.html"
    text = get_text(url)

    if text:
        result = map_reduce(text)
        top_50_words = nlargest(50, result.items(), key=lambda item: item[1])

        print("Топ 50 слів за частотою в тексті:", top_50_words)
        visualize_top_words(dict(top_50_words))
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
