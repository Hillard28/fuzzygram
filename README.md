# fuzzygram
Tool for measuring string similarities based on Jaccard Similarity scoring.  The base method (ratio) is derived from the wonderful [matchit](https://github.com/julioraffo/matchit) ADO created by Julio Raffo.

Will need to run proper benchmarks down the line, but I've been able to process 1,000,000 records using the vector decomposition method in an averaged 47.30 seconds on an i5-8250U with 8MB RAM.  There's certainly room for improvement with the partial matching implementation; the same 1,000,000 records using the vector decomposition method in the partial_ratio function takes me an average XXX seconds!  That's because the ratio is essentially being run 1,000,000 times multiplied by the difference in length between any two strings (with an average length difference of 9.75 characters).  Not to mention this is all pure python using only built-in functions.  For comparison, the partial ratio function of fuzzywuzzy (using normalized Levenshtein distance) takes me 3.11 seconds...
