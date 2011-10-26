"""
K-means.

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

import random

# My favorite number.
#random.seed(23)

class KMeans(Cluster):
    """
    K-means.
    """
    
    def execute(self, docs, clusters=None):
        """
        Main execution.
        
        If clusters are provided, random seeds will not
        be generated.
        
        Key arguments:
        docs     -- the documents to cluster.
        clusters -- initial clusters [optional]
        """
        if clusters == None:
            # Find k random docs to start as our centroids.
            indices = range(len(docs))
            random.shuffle(indices)
            
            # Initialize clusters.
            i = 0
            for index in indices[:self.k]:
                cluster = self.clusters[i]
                docs[index].cluster = cluster
                cluster.docs.append(docs[index])            
                cluster.centroid = self.centroid(self.clusters[i].docs)
                i += 1
        else:
            self.clusters = clusters
        
        change = True
        while change:
            # Check if any of the centroids changed.
            change = False
            
            for doc in docs:
                # Remove this doc from it's original cluster.
                if doc.cluster != None:
                    doc.cluster.docs.remove(doc)
                    doc.cluster = None
                
                max_cluster = None
                max_cos = float("-inf")
                
                # Find the closest cluster for this document.
                for cluster in self.clusters:
                    cos = self.cosine(doc.tfidf, cluster.centroid)
                    if cos > max_cos:                    
                        max_cluster = cluster
                        max_cos = cos
                
                old_centroid = max_cluster.centroid
                   
                # Re-assign this doc the new cluster and find the centroid.
                doc.cluster = max_cluster
                max_cluster.docs.append(doc)            
                max_cluster.centroid = self.centroid(max_cluster.docs)
            
            # Check if the centroid has changed.
            for index in old_centroid:
                if old_centroid[index] - max_cluster.centroid[index] > (1 ** -15):
                    change = True