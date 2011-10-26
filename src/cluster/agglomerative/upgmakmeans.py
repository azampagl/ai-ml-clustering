"""
Agglomerative Hierarchial UPGMA Similarity that seeds K-Means.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 03, CLUSTERING
@copyright Copyright (c) 2011 Aaron Zampaglione
@license MIT
"""
# Dirty hack for Python < 2.5
import sys
sys.path.append('../../')

from cluster.kmeans.core import KMeans
from cluster.lib.dotdict import dotdict
from upgma import AgglomerativeUPGMA

class AgglomerativeUPGMAKMeans(AgglomerativeUPGMA):
    """
    Agglomerative UPGMA with K-Means.
    """
    
    def execute(self, docs):
        """
        Overloads UPGMA's execute and runs the 
        results through K-Means.
        
        Key arguments:
        docs -- the docs to cluster.
        """
        super(AgglomerativeUPGMAKMeans, self).execute(docs)
        
        kmeans = KMeans(self.k)
        kmeans.bible = self.bible
        
        # Clusters will be changed within this method.
        kmeans.execute(docs, self.clusters)