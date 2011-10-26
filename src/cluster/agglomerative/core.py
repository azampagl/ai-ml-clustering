"""
Abstract Agglomerative Hierarchial Clustering.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 03, CLUSTERING
@copyright Copyright (c) 2011 Aaron Zampaglione
@license MIT
"""
# Dirty hack for Python < 2.5
import sys
sys.path.append('../../')

from cluster.core import Cluster
from cluster.lib.dotdict import dotdict

class Agglomerative(Cluster):
    """
    Agglomerative Hierarchial Cluster.
    """
    
    def execute(self, docs):
        """
        @see parent
        """
        # To start, every document is its own cluster.
        clusters = []
        for doc in docs:
            cluster = dotdict()
            
            doc.cluster = cluster
            cluster.docs = []
            cluster.docs.append(doc)
            cluster.centroid = dict(doc.tfidf)
            clusters.append(cluster)
        
        # Continue merging until we reach k clusters.
        while len(clusters) != self.k:
            clusters = self.merge(clusters)
        
        self.clusters = clusters
    
    def merge(self, clusters):
        """
        Merges cluster based on class specific similarity.
        
        Key arguments:
        clusters -- clusters to analyze
        """
        best_sim = float("-inf")
        best_x = None
        best_y = None
        
        clusters_len = len(clusters)
        
        for index1 in range(clusters_len):
            for index2 in range(index1 + 1, clusters_len):
                sim = self.sim(clusters[index1], clusters[index2])
                if sim > best_sim:
                    best_sim = sim
                    best_x = clusters[index1]
                    best_y = clusters[index2]
        
        # Remove one of the clusters we're going to merge.
        clusters.remove(best_y)
        
        # Extend the documents.
        best_x.docs.extend(best_y.docs)
        best_x.centroid = self.centroid(best_x.docs)
        
        # Reset the doc's clusters to the new merged cluster.
        for doc in best_y.docs:
            doc.cluster = best_x
        
        return clusters
    
    # ABSTRACT
    def sim(self, cluster1, cluster2):
        """
        Class specific similarity measure.
        
        Key arguments:
        cluster1 -- first cluster.
        cluster2 -- second cluster.
        """
        pass