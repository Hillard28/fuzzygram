"""
Tool for measuring string similarities based on Jaccard Similarity
Currently supports either unigram or moving-bigram matching
"""


def ratio(string1, string2, type="vector"):
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
        elif type == "loose":
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
        elif type == "strict":
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
                # lstring_hold = []
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
        


def partial_ratio(string1, string2):
    if string1 == "" and string2 == "":
        score = 1.0
        return score
    elif (
        (string1 != "" and string2 == "")
        or (string1 == "" and string2 != "")
        or (len(string1) == 1 or len(string2) == 1)
    ):
        score = 0.0
        return score
    elif len(string1) == len(string2):
        return ratio(string1, string2)
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
        scores = []
        lstring_hold = []
        while len(sstring) < len(lstring):
            lstring_hold.append(lstring.pop(-1))
        dot = []
        for entry1, entry2 in zip(sstring, lstring):
            if entry1 == entry2:
                dot.append(1)
            else:
                dot.append(0)
        score = sum(dot) / ((len(sstring)) * (len(lstring))) ** (1 / 2)
        scores.append(score)
        while iterations > 0:
            lstring.append(lstring_hold.pop(-1))
            lstring_hold.insert(0, lstring.pop(0))
            dot = []
            for entry1, entry2 in zip(sstring, lstring):
                if entry1 == entry2:
                    dot.append(1)
                else:
                    dot.append(0)
            score = sum(dot) / ((len(sstring)) * (len(lstring))) ** (1 / 2)
            scores.append(score)
            iterations -= 1
        return max(scores)
