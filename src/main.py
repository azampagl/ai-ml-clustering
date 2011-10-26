"""
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

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 03, CLUSTERING
@copyright Copyright (c) 2011 Aaron Zampaglione
@license MIT
"""
from cluster.doc import Doc
from cluster.lib.dotdict import dotdict

import getopt
import os
import re
import sys

# Maps user input to the proper algorithm.
CLUSTERS = {'k-means': ['kmeans.core', 'KMeans'],
            'bi-k-means-size': ['bikmeans.size', 'BiKMeansSize'],
            'bi-k-means-sim': ['bikmeans.sim', 'BiKMeansSim'],
            'agg-ist': ['agglomerative.ist', 'AgglomerativeIST'],
            'agg-cst': ['agglomerative.cst', 'AgglomerativeCST'],
            'agg-upgma': ['agglomerative.upgma', 'AgglomerativeUPGMA'],
            'agg-upgma-k-means': ['agglomerative.upgmakmeans', 'AgglomerativeUPGMAKMeans'],
            }

def init(topic_file):
    """
    Parses a topic file and returns all of the documents
    and the list of words in it.
    
    Key arguments:
    topic_file -- the topic file.
    """
    bible = dotdict()
    bible.topics = {}
    bible.words = dotdict()  
    docs = []
    
    dir = os.path.dirname(topic_file)
    
    topic_handle = open(topic_file, 'r')
    for topic in topic_handle:
        if topic == "\n":
            continue
        
        topic = topic[:-1]
                
        # Read in each topic file.
        docs_file = dir + '/' + topic + '.txt'
        docs_handle = open(docs_file, 'r')
        
        # Add a new topic to the bible.
        topic = topic.upper()
        bible.topics[topic] = []
        
        # Split the file based on the document id and its text.
        split = re.split(r"(--\w+--)", str(docs_handle.read()), re.I | re.M)[1:]
        
        # For each document, find all the words.
        i = 0
        while i < len(split):
            id = split[i][2:-2]
            words = re.findall(r'\w+', split[i + 1].upper())
            doc = Doc.factory(topic, id, words, bible)
            docs.append(doc)
            bible.topics[topic].append(doc)
            i += 2
        
        docs_handle.close()
    
    topic_handle.close()
    
    # Run through each document and init the TFIDF vector.
    for doc in docs:
        doc.init(bible)
    
    # Set the docs in the bible
    bible.docs = docs
    
    return bible, docs

def main():
    """Main execution method."""
    # Determine command line arguments.
    try:
        rawopts, _ = getopt.getopt(sys.argv[1:], "t:a:k:i:o:r:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    opts = {}
    # Process each command line argument.
    for o, a in rawopts:
        opts[o[1]] = a
    
    # The following arguments are required in all cases.
    for opt in ['t', 'a', 'k', 'o', 'r']:
        if not opt in opts:
            usage()
            sys.exit(2)
    
    params = []
    
    # Check if algorithm exists.
    if opts['k'] in CLUSTERS:
        usage()
        sys.exit(2)
    
    # Add k to params list.
    params.append(str(int(opts['k'])))
    
    # Check if ITER is required.
    if opts['a'] in ['bi-k-means-size', 'bi-k-means-sim']:
        if not 'i' in opts:
            usage()
            sys.exit(2)
        
        opts['i'] = int(opts['i'])
        # Add iter to params list.
        params.append(str(int(opts['i'])))
    
    # Parse all the documents and find all the words (bible).
    bible, docs = init(opts['t'])
    
    m = 'cluster.' + CLUSTERS[opts['a']][0]
    c = m + '.' + CLUSTERS[opts['a']][1]
    
    exec('import ' + m)
    exec('model = ' + c + '(' + ', '.join(params) + ')')
    # Inject the bible into the model.
    model.bible = bible
    
    # Output the TFIDF.
    output = ""
    for doc in bible.docs:
        output += str(doc)
    tfidf_file = open(opts['o'], 'w')
    tfidf_file.write(output)
    tfidf_file.close()
    
    # Execute the model, output the results and evaluation.
    model.execute(docs)
    model.results(opts['r'])
    print(model.evaluate())

def usage():
    """Prints the usage of the program."""
    print("\n" + 
          "The following are arguments required:\n" + 
          "-t: the topic file.\n" + 
          "-a: the clustering algorithm (" + ', '.join(CLUSTERS.keys()) + ").\n" + 
          "-k: the number of clusters\n" + 
          "-o: the TFIDF file.\n" + 
          "-r: the result file.\n\n" + 
          "The following arguments are required for bisecting k-means algorithms:\n"
          "-i: number of iterations.\n" +
          "\n" + 
          "Example Usage:\n" + 
          "python main.py -t \"../data/toy/toy-topics.txt\" -a \"k-means\" -k 3 " + 
          "-o \"../results/toy/tfidf.dat\" -r \"../results/toy/k-means.txt\"" + 
          "\n")

"""Main execution."""
if __name__ == "__main__":
    main()