"""
Bisecting K-means with least overall similarity.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 03, CLUSTERING
@copyright Copyright (c) 2011 Aaron Zampaglione
@license MIT
"""
from core import BiKMeans

class BiKMeansSim(BiKMeans):
    """
    Bisecting K-Means by Similarity.
    """
    
    def select_cluster(self, clusters):
        """
        Selects cluster based on least similarity.
        
        Key arguments:
        clusters -- clusters to analyze.
        """
        min_sim = float("inf")
        min_cluster = None
        
        for cluster in clusters:
            sim = 0.0
            for index, value in cluster.centroid.items():
                sim += value * value
            
            if sim < min_sim:
                min_sim = sim
                min_cluster = cluster
        
        return min_cluster