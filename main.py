import string
from collections import defaultdict

import requests
from bs4 import BeautifulSoup


def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text

    return html_content


def k_most_frequent_words(url, excluded_words, k=10):
    soup = BeautifulSoup(get_content(url), 'html.parser')
    excluded_words = set(excluded_words)
    excluded_words.add('')
    word_count = defaultdict(int)
    start_tag = 'arbitrary Html id'
    end_tag = 'arbitrary Html id'
    start = soup.find(id=start_tag)
    end = soup.find(id=end_tag)
    element = start
    while element != end:
        text = element.get_text()
        if text:
            words_in_text = text.split(' ')
            for word in words_in_text:
                word = word.rstrip(string.punctuation)
                if word in excluded_words:
                    continue
                word_count[word] += 1
        element = element.next_element

    most_freq = sorted(word_count.items(), reverse=True, key=lambda x: x[1])
    return most_freq[:k]


if __name__ == '__main__':
    website = 'https://en.wikipedia.org/wiki/Fake_Page'
    num_of_words = input("How many top words? Leave blank for default of 10.")
    if num_of_words == '':
        num_of_words = 10
    else:
        num_of_words = int(num_of_words)
    raw_exclude = str(
        input("Separated by commas, enter all case sensitive words that you want excluded from the search."))
    exclude = [word.strip() for word in raw_exclude.split(',')]

    print(k_most_frequent_words(website, exclude, num_of_words))
