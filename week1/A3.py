# Генератор chunked(iterable, n)
# Ленивая функция-генератор: режет любой итерируемый объект на куски по n.
# list(chunked(range(7), 3)) → [[0,1,2],[3,4,5],[6]].
# Запрещено предварительно превращать вход в список целиком — вход может быть бесконечным генератором.

def chunked(iterator, n: int):
    chunk = []
    for i in iterator:
        chunk.append(i)
        if len(chunk) == n:
            yield chunk
            chunk = []
    else:
        yield chunk

if __name__ == '__main__':
    print(list(chunked(range(7), 3)))