# fuzzygram
Tool for measuring string similarities based on Jaccard Similarity scoring.  The base method (ratio) is derived from the wonderful [matchit](https://github.com/julioraffo/matchit) ADO created by Julio Raffo.

Will need to run proper benchmarks down the line, but I've been able to process 5 million records using the vector decomposition method in around 6.5 minutes on an i5-8250U with 8MB RAM.
