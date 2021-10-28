"""
Tool for measuring string similarities based on Jaccard Similarity
Currently supports either unigram or moving-bigram matching
"""
from itertools import tee
from collections import Counter

def bigram(iterable):
    c1, c2 = tee(iterable)
    next(c2, None)
    return tuple(zip(c1, c2))

def ratio(string1, string2, match="vector"):
    """
    Compare both string inputs in their entirety.
    Type determines what method is used to compare:
    Vector: vector decomposition into vectors of moving bigrams, with both
    strings scored on frequency of the bigrams present in their union
    Loose: each bigram treated as unique entity, with a score of 1 or 0 being
    assigned depending on presence. If strings of different length are compared
    the algorithm compares the bigrams of the smaller string to the larger
    Strict: order matters. Each string's bigram in a given position is compared
    to the bigram in the same position of the other string. If strings are of
    different lengths, the smaller string is rolled across the larger string to
    compare all possible alignments and the highest score is selected.
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
            string1 = Counter(bigram(string1))
            string2 = Counter(bigram(string2))
            dot = sum(string1[i]*string2[i] for i in string1.keys() | string2.keys())
            norm1 = sum([i**2 for i in string1.values()])
            norm2 = sum([i**2 for i in string2.values()])
            return dot / ((norm1 * norm2)**(0.5))
        elif match == "loose":
            if len(string1) == len(string2):
                string1 = [string1[i : i + 2] for i in range(0, len(string1) - 1)]
                string2 = [string2[i : i + 2] for i in range(0, len(string2) - 1)]
                string2_comp = string2[:]
                dot = []
                for entry in string1:
                    if entry in string2_comp:
                        dot.append(1)
                        string2_comp.remove(entry)
                    else:
                        dot.append(0)
                score = sum(dot) / ((len(string1) * len(string2))**(0.5))
                return score
            else:
                if len(string1) < len(string2):
                    sstring = [string1[i : i + 2] for i in range(0, len(string1) - 1)]
                    lstring = [string2[i : i + 2] for i in range(0, len(string2) - 1)]
                elif len(string1) > len(string2):
                    sstring = [string2[i : i + 2] for i in range(0, len(string2) - 1)]
                    lstring = [string1[i : i + 2] for i in range(0, len(string1) - 1)]
                lstring_comp = lstring[:]
                dot = []
                for entry in sstring:
                    if entry in lstring_comp:
                        dot.append(1)
                        lstring_comp.remove(entry)
                    else:
                        dot.append(0)
                return sum(dot) / ((len(sstring) * len(lstring))**(0.5))
        elif match == "strict":
            if len(string1) == len(string2):
                string1 = bigram(string1)
                string2 = bigram(string2)
                dot = []
                for entry1, entry2 in zip(string1, string2):
                    if entry1 == entry2:
                        dot.append(1)
                    else:
                        dot.append(0)
                return sum(dot) / ((len(string1) * len(string2))**(0.5))
            else:
                if len(string1) < len(string2):
                    sstring = bigram(string1)
                    lstring = bigram(string2)
                else:
                    sstring = bigram(string2)
                    lstring = bigram(string1)
                rightpad = len(sstring) - len(lstring)
                leftpad = 0
                scores = []
                while rightpad < 0:
                    dot = []
                    for entry1, entry2 in zip(sstring, lstring):
                        if entry1 == entry2:
                            dot.append(1)
                        else:
                            dot.append(0)
                    scores.append(sum(dot) / ((len(sstring) * len(lstring))**(0.5)))
                    rightpad += 1
                    leftpad += 1
                return max(scores)
        


def partial_ratio(string1, string2, match="vector"):
    """
    Compare both string inputs within a window determined by the smaller string.
    Here, the excess length of the larger string is
    clipped, then sequentially re-added while stripping away corresponding
    bigrams from the left side. In this way, the smaller string is compared to
    a rolling window of the larger string.
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
        if len(string1) < len(string2):
            sstring = bigram(string1)
            lstring = bigram(string2)
        else:
            sstring = bigram(string2)
            lstring = bigram(string1)
        rightpad = len(sstring) - len(lstring)
        leftpad = 0
        scores = []
        if match == "vector":
            while rightpad < 0:
                scount = Counter(sstring)
                lcount = Counter(lstring[leftpad:rightpad])
                dot = sum(scount[i]*lcount[i] for i in scount.keys() | lcount.keys())
                snorm = sum([i**2 for i in scount.values()])
                lnorm = sum([i**2 for i in lcount.values()])
                scores.append(dot / ((snorm * lnorm)**(0.5)))
                rightpad += 1
                leftpad += 1
            return max(scores)
        elif match == "strict":
            while rightpad < 0:
                dot = []
                for entry1, entry2 in zip(sstring, lstring[leftpad:rightpad]):
                    if entry1 == entry2:
                        dot.append(1)
                    else:
                        dot.append(0)
                scores.append(sum(dot) / len(sstring))
                rightpad += 1
                leftpad += 1
            return max(scores)
