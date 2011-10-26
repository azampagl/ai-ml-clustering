"""
Agglomerative Hierarchial UPGMA Similarity.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 03, CLUSTERING
@copyright Copyright (c) 2011 Aaron Zampaglione
@license MIT
"""
# Dirty hack for Python < 2.5
import sys
sys.path.append('../../')

from cluster.lib.dotdict import dotdict
from core import Agglomerative

class AgglomerativeUPGMA(Agglomerative):
    """
    Agglomerative Hierarchial UPGMA Similarity.
    """
    
    def sim(self, cluster1, cluster2):
        """
        @see parent
        """
        sim = 0.0
        for doc1 in cluster1.docs:
            for doc2 in cluster2.docs:
                sim += self.cosine(doc1.tfidf, doc2.tfidf)
        
        return sim / (len(cluster1.docs) * len(cluster2.docs))