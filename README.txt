============================================
Python Clustering

Aaron Zampaglione
CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
Proj 03, CLUSTERING
============================================

Python implementation of the different clustering algorithms.

A Comparison of Document Clustering Techniques

Michael Steinbach, George Karypis, Vipin Kumar 
Department of Computer Science and Egineering, 
University of Minnesota 
Technical Report #00-034 
{steinbac, karypis, kumar}@cs.umn.edu
@see http://www.cs.fit.edu/~pkc/classes/ml-internet/papers/steinbach00tr.pdf

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

"Modules".
1. Preprocess: occurs in the init method.
2. Cluster: occurs via the classes "execute" method.
3. Evaluate: occurs during the classes "evaluate" method.


============================================
Arguments for python main.py
============================================


	The following are arguments required:

-t: the topic file.
-a: the clustering algorithm (agg-upgma-k-means, agg-cst, k-means, bi-k-means-size, agg-ist, bi-k-means-sim, agg-upgma).
-k: the number of clusters
-o: the TFIDF file.
-r: the result file.

	The following arguments are required for bisecting k-means algorithms:

-i: number of iterations.


============================================
Execution
============================================

	Execution is straightforward.  After choosing a topic file (-t), a clustering algorithm (-a), and the number of clusters (-k), the program will spit out the TFIDF vectors for each document (-o) and the results (-r).

======================
	Usage
======================

	The following are some example use cases.

> python main.py -t "../data/toy/toy-topics.txt" -a "k-means" -k 3 -o "../results/toy/tfidf.dat" -r "../results/toy/k-means.txt"
