from itertools import islice

def try_extract(d,field):
    try:
        return d[field]
    except Exception:
        return None

def chunker(iterable, n):
    iterable = iter(iterable)
    count = 0
    group = []
    while True:
        try:
            group.append(iterable.next())
            count += 1
            if count % n == 0:
                yield group
                group = []
        except StopIteration:
            yield group
            brea
