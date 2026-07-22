# Дан текст. Топ-5 частых слов (регистр игнорировать, пунктуацию убрать) в формате
# «слово:количество». Двумя способами: Counter и вручную через defaultdict(int); сравнить код
from collections import Counter, defaultdict
from string import punctuation


def normalize(text: str) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("Неверный тип текста")
    return text.lower().translate(str.maketrans('', '', punctuation)).split()


# Counter
def word_counter(text: str) -> dict[str: int]:
    text = normalize(text)  # type(text) = list
    count = Counter(text)

    return dict(count.most_common(5))


# defaultdict
def word_default(text: str) -> dict[str: int]:
    text = normalize(text)  # type(text) = list
    count = defaultdict(int)
    for word in text:
        count[word] += 1

    top_words = sorted(count.keys(), key=count.get, reverse=True)[:5]
    return {word: count[word] for word in top_words}
