"""
Agglomerative Hierarchial Centroid Similarity.

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

class AgglomerativeCST(Agglomerative):
    """
    Agglomerative Hierarchial Centroid Similarity.
    """
    
    def sim(self, cluster1, cluster2):
        """
        @see parent
        """
        return self.cosine(cluster1.centroid, cluster2.centroid)