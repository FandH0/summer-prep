# Дан текст. Топ-5 частых слов (регистр игнорировать, пунктуацию убрать) в формате
# «слово:количество». Двумя способами: Counter и вручную через defaultdict(int); сравнить код
from collections import Counter, defaultdict
# Counter
def word_counter(text: str):
    if not isinstance(text, str): raise ValueError

    punc = (',', ',', '!', '?', ';', '"', "'")
    for i in punc:
        text = text.replace(i, '')

    text = text.lower()   # type(text) = str
    text = text.split()   # type(text) = list
    text = Counter(text)  # type(text) = Counter i.e word:count

    top_words = sorted(text.keys(), key=text.get, reverse=True)[:5]
    return {word: text[word] for word in top_words}

# defaultdict
def word_default(text: str):
    if not isinstance(text, str): raise ValueError

    punc = (',', ',', '!', '?', ';', '"', "'")
    for i in punc:
        text = text.replace(i, '')

    text = text.lower()   # type(text) = str
    text = text.split()   # type(text) = list
    count = defaultdict(int)
    for word in text:
        count[word] += 1

    top_words = sorted(count.keys(), key=count.get, reverse=True)[:5]
    return {word: count[word] for word in top_words}

if __name__ == "__main__":
    example = "This example shows how the __missing__() method works behind the scenes in defaultdict. \n It is automatically called when a key is not found, returning the default value instead of raising a KeyError."
    assert word_counter(example) == word_default(example)