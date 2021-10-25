# fuzzygram
Tool for measuring string similarities based on Jaccard Similarity scoring.  The base method (ratio) is derived from the wonderful [matchit](https://github.com/julioraffo/matchit) ADO created by Julio Raffo.

Will need to run proper benchmarks down the line, but I've been able to process 5 million records using the vector decomposition method in around 6.5 minutes on an i5-8250U with 8MB RAM.  There's certainly room for improvement with the partial matching implementation; the same 5 million records using the vector decomposition method in the partial_ratio function takes me ~28 minutes!  That's because the ratio is essentially being run 5 million times multiplied by the difference in length between any two strings.
