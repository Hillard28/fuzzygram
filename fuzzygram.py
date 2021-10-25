"""
Tool for measuring string similarities based on Jaccard Similarity
Currently supports either unigram or moving-bigram matching
"""


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
            string1 = [string1[i : i + 2] for i in range(0, len(string1) - 1)]
            string2 = [string2[i : i + 2] for i in range(0, len(string2) - 1)]
            unionset = set(set(string1) | set(string2))
            sim1 = []
            sim2 = []
            for x in unionset:
                sim1.append(string1.count(x))
                sim2.append(string2.count(x))
            dot = sum(i[0]*i[1] for i in zip(sim1, sim2))
            norm1 = sum([i**2 for i in sim1])**(1/2)
            norm2 = sum([i**2 for i in sim2])**(1/2)
            score = dot / (norm1 * norm2)
            return score
        elif match == "loose":
            if len(string1) == len(string2):
                string1 = [string1[i : i + 2] for i in range(0, len(string1) - 1)]
                string2 = [string2[i : i + 2] for i in range(0, len(string2) - 1)]
                dot = []
                for entry in string1:
                    if entry in string2:
                        dot.append(1)
                        string2.remove(entry)
                    else:
                        dot.append(0)
                score = sum(dot) / ((len(string1)) * (len(string2))) ** (
                    1 / 2
                )
                return score
            else:
                if len(string1) < len(string2):
                    sstring = string1
                    lstring = string2
                elif len(string1) > len(string2):
                    sstring = string2
                    lstring = string1
                sstring = [sstring[i : i + 2] for i in range(0, len(sstring) - 1)]
                lstring = [lstring[i : i + 2] for i in range(0, len(lstring) - 1)]
                lstring_comp = lstring[:]
                dot = []
                for entry in sstring:
                    if entry in lstring_comp:
                        dot.append(1)
                        lstring_comp.remove(entry)
                    else:
                        dot.append(0)
                score = sum(dot) / ((len(sstring)) * (len(lstring))) ** (
                    1 / 2
                )
                return score
        elif match == "strict":
            if len(string1) == len(string2):
                string1 = [string1[i : i + 2] for i in range(0, len(string1) - 1)]
                string2 = [string2[i : i + 2] for i in range(0, len(string2) - 1)]
                dot = []
                for entry1, entry2 in zip(string1, string2):
                    if entry1 == entry2:
                        dot.append(1)
                    else:
                        dot.append(0)
                score = sum(dot) / ((len(string1)) * (len(string2))) ** (
                    1 / 2
                )
                return score
            else:
                if len(string1) < len(string2):
                    sstring = string1
                    lstring = string2
                elif len(string1) > len(string2):
                    sstring = string2
                    lstring = string1
                sstring = [sstring[i : i + 2] for i in range(0, len(sstring) - 1)]
                lstring = [lstring[i : i + 2] for i in range(0, len(lstring) - 1)]
                iterations = len(lstring) - len(sstring)
                adjust = len(lstring) - len(sstring)
                scores = []
                while len(sstring) < len(lstring):
                    sstring.append("")
                dot = []
                for entry1, entry2 in zip(sstring, lstring):
                    if entry1 == entry2:
                        dot.append(1)
                    else:
                        dot.append(0)
                score = sum(dot) / ((len(sstring) - adjust) * (len(lstring))) ** (1 / 2)
                scores.append(score)
                while iterations > 0:
                    sstring.insert(0, sstring.pop(-1))
                    dot = []
                    for entry1, entry2 in zip(sstring, lstring):
                        if entry1 == entry2:
                            dot.append(1)
                        else:
                            dot.append(0)
                    score = sum(dot) / ((len(sstring) - adjust) * len(lstring)) ** (1 / 2)
                    scores.append(score)
                    iterations -= 1
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
        if match == "vector":
            if len(string1) < len(string2):
                sstring = string1
                lstring = string2
            elif len(string1) > len(string2):
                sstring = string2
                lstring = string1
            sstring = [sstring[i : i + 2] for i in range(0, len(sstring) - 1)]
            lstring = [lstring[i : i + 2] for i in range(0, len(lstring) - 1)]
            rightpad = len(sstring) - len(lstring)
            leftpad = 0
            scores = []
            unionset = set(set(sstring) | set(lstring[leftpad:rightpad]))
            sim1 = []
            sim2 = []
            for x in unionset:
                sim1.append(string1.count(x))
                sim2.append(string2.count(x))
            dot = sum(i[0]*i[1] for i in zip(sim1, sim2))
            norm1 = sum([i**2 for i in sim1])**(1/2)
            norm2 = sum([i**2 for i in sim2])**(1/2)
            score = dot / (norm1 * norm2)
            scores.append(score)
            rightpad += 1
            leftpad += 1
            while rightpad < 0:
                unionset = set(set(sstring) | set(lstring[leftpad:rightpad]))
                sim1 = []
                sim2 = []
                for x in unionset:
                    sim1.append(string1.count(x))
                    sim2.append(string2.count(x))
                dot = sum(i[0]*i[1] for i in zip(sim1, sim2))
                norm1 = sum([i**2 for i in sim1])**(1/2)
                norm2 = sum([i**2 for i in sim2])**(1/2)
                score = dot / (norm1 * norm2)
                scores.append(score)
                rightpad += 1
                leftpad += 1
            return max(scores)
        elif match == "strict":
            if len(string1) < len(string2):
                sstring = string1
                lstring = string2
            elif len(string1) > len(string2):
                sstring = string2
                lstring = string1
            sstring = [sstring[i : i + 2] for i in range(0, len(sstring) - 1)]
            lstring = [lstring[i : i + 2] for i in range(0, len(lstring) - 1)]
            rightpad = len(sstring) - len(lstring)
            leftpad = 0
            scores = []
            dot = []
            for entry1, entry2 in zip(sstring, lstring[leftpad:rightpad]):
                if entry1 == entry2:
                    dot.append(1)
                else:
                    dot.append(0)
            score = sum(dot) / ((len(sstring)) * (len(lstring))) ** (1 / 2)
            scores.append(score)
            rightpad += 1
            leftpad += 1
            while rightpad < 0:
                dot = []
                for entry1, entry2 in zip(sstring, lstring[leftpad:rightpad]):
                    if entry1 == entry2:
                        dot.append(1)
                    else:
                        dot.append(0)
                score = sum(dot) / ((len(sstring)) * (len(lstring))) ** (1 / 2)
                scores.append(score)
                rightpad += 1
                leftpad += 1
            return max(scores)
