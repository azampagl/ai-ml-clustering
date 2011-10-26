"""
Bisecting K-means with largest cluster to split.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 03, CLUSTERING
@copyright Copyright (c) 2011 Aaron Zampaglione
@license MIT
"""
from core import BiKMeans

class BiKMeansSize(BiKMeans):
    """
    Bisecting K-Means by Size.
    """
    
    def select_cluster(self, clusters):
        """
        Selects cluster based on size.
        
        Key arguments:
        clusters -- clusters to analyze.
        """
        max_len = 0
        max_cluster = None
        
        for cluster in clusters:
            cluster_len = len(cluster.docs)
            if cluster_len > max_len:
                max_len = cluster_len
                max_cluster = cluster
        
        return max_cluster