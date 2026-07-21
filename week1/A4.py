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
    text = normalize(text) # type(text) = list
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


if __name__ == "__main__":
    example = "This example shows how the __missing__() method works behind the scenes in defaultdict. \n It is automatically called when a key is not found, returning the default value instead of raising a KeyError."
    assert word_counter(example) == word_default(example)
    assert word_counter('a, a , d a f f') == {'a': 3, 'f': 2, 'd': 1}
    assert word_default('a, a , d a f f') == {'a': 3, 'f': 2, 'd': 1}