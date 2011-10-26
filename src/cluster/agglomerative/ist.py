"""
Agglomerative Hierarchial Intra-Cluster Similarity.

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

class AgglomerativeIST(Agglomerative):
    """
    Agglomerative Hierarchial Intra-Cluster Similarity.
    """
    
    def sim(self, cluster1, cluster2):
        """
        @see parent
        """
        sim1 = 0.0
        for doc in cluster1.docs:
            sim1 += self.cosine(doc.tfidf, cluster1.centroid)
        
        sim2 = 0.0
        for doc in cluster2.docs:
            sim2 += self.cosine(doc.tfidf, cluster2.centroid)
        
        docs = list(cluster1.docs)
        docs.extend(cluster2.docs)
        centroid = self.centroid(docs)
        
        sim3 = 0.0
        for doc in docs:
            sim3 += self.cosine(doc.tfidf, centroid)
        
        return sim3 - sim1 - sim2