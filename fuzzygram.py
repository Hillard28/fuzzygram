"""
Tool for measuring string similarities based on Jaccard Similarity
Currently supports either unigram or moving-bigram matching
"""
from collections import Counter
from itertools import tee, chain

def window(iterable, width):
    a, b, c, d = tee(iterable, 4)
    a = chain([None], a) # prepend None
    next(d, None)
    for x in range(width - 2):
        next(c, None)
        next(d, None)
    return zip(zip(a, b), zip(c, d))

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def ratio(string1, string2, match="vector"):
    """
    Compare both string inputs in their entirety.
    "match" will eventually determine what method is used to compare:
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
        if match == "vector":
            string1 = Counter(pairwise(string1))
            string2 = Counter(pairwise(string2))
            dot = sum(string1[i]*string2[i] for i in string1.keys())
            norm1 = sum([i**2 for i in string1.values()])
            norm2 = sum([i**2 for i in string2.values()])
            return dot / ((norm1 * norm2)**(0.5))

def partial_ratio(string1, string2, match="vector"):
    """
    Compare both string inputs within a window determined by the smaller string.
    The excess length of the larger string is clipped, then sequentially re-added
    while stripping away corresponding bigrams from the left side. In this way,
    the smaller string is compared to a rolling window of the larger string.
    Here, comparison of "xyz" and "xyz excess characters", will return a score
    of ~1, while the non-partial comparisons will factor in the excess.
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
        return ratio(string1, string2, match)
    else:
        if match == "vector":
            if len(string1) < len(string2):
                sstring = string1
                lstring = string2
            else:
                sstring = string2
                lstring = string1
            bigram = Counter(pairwise(sstring))
            snorm = sum(i**2 for i in bigram.values())
            window_size = len(sstring)
            target = Counter(pairwise(lstring[:window_size]))
            target[(None, lstring[0])] += 1
            target[(lstring[window_size - 2], lstring[window_size - 1])] -= 1
            results = {}
            for index, (old, new) in enumerate(window(lstring, window_size)):
                target[old] -= 1
                target[new] += 1
                dot = sum(count*target[key] for key, count in bigram.items())
                norm = (sum(i**2 for i in target.values() if i > 0) * snorm) ** 0.5
                results[index] = dot/norm
            return max(results.values())
