# Генератор chunked(iterable, n)
# Ленивая функция-генератор: режет любой итерируемый объект на куски по n.
# list(chunked(range(7), 3)) → [[0,1,2],[3,4,5],[6]].
# Запрещено предварительно превращать вход в список целиком — вход может быть бесконечным генератором.

def chunked(iterable, n: int):
    if not n > 0:
        raise ValueError("Negative chunks unsupported")
    chunk = []
    for i in iterable:
        chunk.append(i)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
