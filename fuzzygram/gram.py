"""
Tool for measuring string similarities based on Jaccard Similarity
Currently supports either unigram or moving-bigram matching
"""
from collections import Counter
from itertools import tee, chain


def window(iterable, width):
    a, b, c, d = tee(iterable, 4)
    a = chain([None], a)  # prepend None
    next(d, None)
    for x in range(width - 2):
        next(c, None)
        next(d, None)
    return zip(zip(a, b), zip(c, d))


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def ratio(string1, string2, type="vector"):
    """
    Compare both string inputs in their entirety.
    "type" will eventually determine what method is used to compare:
    Vector: decomposition of strings into vectors of moving bigrams, with
    both strings scored on frequency of the bigrams present in their union
    """
    if string1 == "" and string2 == "":
        return 1.0
    elif (
        (string1 != "" and string2 == "")
        or (string1 == "" and string2 != "")
        or (len(string1) == 1 or len(string2) == 1)
    ):
        return 0.0
    else:
        if type == "vector":
            string1 = Counter(pairwise(string1))
            string2 = Counter(pairwise(string2))
            dot = sum(string1[i] * string2[i] for i in string1.keys())
            norm1 = sum([i ** 2 for i in string1.values()])
            norm2 = sum([i ** 2 for i in string2.values()])
            return dot / ((norm1 * norm2) ** (0.5))


def partial_ratio(string1, string2, type="vector", method="window"):
    """
    Compare both string inputs within a window determined by the smaller
    string. A window the size of the smaller string is rolled across the larger
    string and similarity score is computed at each step. The largest score is
    then returned. Here, comparison of "xyz" and "xyz excess", will return a
    score of ~1, while the non-partial comparisons will penalize excess.
    """
    if string1 == "" and string2 == "":
        return 1.0
    elif (
        (string1 != "" and string2 == "")
        or (string1 == "" and string2 != "")
        or (len(string1) == 1 or len(string2) == 1)
    ):
        return 0.0
    elif len(string1) == len(string2):
        return ratio(string1, string2, type)
    else:
        if type == "vector":
            if method == "window":
                if len(string1) < len(string2):
                    sstring = string1
                    lstring = string2
                else:
                    sstring = string2
                    lstring = string1
                bigram = Counter(pairwise(sstring))
                snorm = sum(i ** 2 for i in bigram.values())
                window_size = len(sstring)
                target = Counter(pairwise(lstring[:window_size]))
                target[(None, lstring[0])] += 1
                target[(lstring[window_size - 2], lstring[window_size - 1])] -= 1
                results = {}
                for index, (old, new) in enumerate(window(lstring, window_size)):
                    target[old] -= 1
                    target[new] += 1
                    dot = sum(count * target[key] for key, count in bigram.items())
                    norm = (sum(i ** 2 for i in target.values() if i > 0) * snorm) ** 0.5
                    results[index] = dot / norm
                return max(results.values())
            elif method == "shorter":
                if len(string1) < len(string2):
                    sstring = pairwise(string1)
                    lstring = list(pairwise(string2))
                else:
                    sstring = pairwise(string2)
                    lstring = list(pairwise(string1))
                results = []
                for bigram in sstring:
                    if bigram in lstring:
                        results.append(1)
                        lstring.remove(bigram)
                    else:
                        results.append(0)
                return sum(results) / len(results)
