"""
Abstract Bisecting K-Means class.

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
from cluster.kmeans.core import KMeans
from cluster.lib.dotdict import dotdict

class BiKMeans(Cluster):
    """
    Bi-K-Means
    """
    
    # Number of iterations.
    iter = 0
    
    def __init__(self, k, iter):
        """
        Init.
        
        Key arguments:
        k    -- final number of clusters.
        iter -- number of iterations.
        """
        super(BiKMeans, self).__init__(k)
        
        self.iter = iter
    
    def execute(self, docs):
        """
        @see parent
        """
        clusters = []
        
        # First cluster contains all of the docs.
        cluster = dotdict()
        cluster.docs = []
        
        for doc in self.bible.docs:
            doc.cluster = cluster
            cluster.docs.append(doc)
        
        cluster.centroid = self.centroid(cluster.docs)
        
        # Append the first cluster to the cluster list.
        clusters.append(cluster)
        
        while len(clusters) != self.k:
            # Use the abstract select cluster method.
            cluster = self.select_cluster(clusters)
                        
            # Remove this cluster from the current set because it will be split.
            clusters.remove(cluster)
            
            max_sim = float("-inf")
            max_bicluster = None
                        
            for i in range(self.iter):
                # Free the docs from whatever cluster they are in.
                for doc in cluster.docs:
                    doc.cluster = None
                
                kmeans = KMeans(2)
                kmeans.bible = self.bible
                
                kmeans.execute(cluster.docs)
                bicluster = kmeans.clusters
                
                sim = kmeans.similarity()
                if sim > max_sim:
                    max_sim = sim
                    max_bicluster = bicluster
            
            # Re-assign the documents to their respective max bicluster.
            for cluster in bicluster:
                for doc in cluster.docs:
                    doc.cluster = cluster
            
            # Add the new max bicluster to the current cluster set.
            clusters.extend(bicluster)
        
        self.clusters = clusters
    
    # ABSTRACT
    def select_cluster(self, clusters):
        """
        Class specific cluster selection.
        
        Key arguments:
        clusters -- clusters to analyze.
        """
        pass