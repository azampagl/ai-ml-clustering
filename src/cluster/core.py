"""
Abstract class for a cluster solution.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 03, CLUSTERING
@copyright Copyright (c) 2011 Aaron Zampaglione
@license MIT
"""
from doc import Doc
from lib.dotdict import dotdict

import math

class Cluster(object):
    """
    """
    
    @classmethod
    def centroid(cls, docs):
        """
        Returns the centroid value for a set of documents.
        
        Key arguments:
        docs -- the set of documents
        """
        centroid = dict(docs[0].tfidf)
        
        for doc in docs[1:]:
            for index in doc.tfidf:
                centroid[index] += doc.tfidf[index]
        
        docs_len = float(len(docs))
        
        for index in centroid:
            centroid[index] = centroid[index] / docs_len 
        
        return centroid
    
    @classmethod
    def cosine(cls, vector1, vector2):
        """
        Return the cosine between two documents
        
        Key arguments:
        vector1 -- first vector.
        vector2 -- second vector.
        """
        prod = 0.0
        
        mag1 = 0.0
        mag2 = 0.0
        
        for index in vector1:
            prod += vector1[index] * vector2[index]
            mag1 += vector1[index] * vector1[index]
            mag2 += vector2[index] * vector2[index]
        
        return prod / (math.sqrt(mag1) * math.sqrt(mag2))
    
    # Word dictionary.
    bible = None
    
    # Final number of clusters.
    k = 0
    
    # Clusters
    clusters = []
    
    def __init__(self, k):
        """
        Init.
        
        Key arguments:
        k -- final number of clusters.
        """
        self.k = k
        
        self.clusters = []
        for i in range(k):
            self.clusters.append(dotdict())
            self.clusters[-1].docs = []
    
    def entropy(self):
        """
        Calculates the entroy of this cluster solution.
        """
        sum = 0.0
        for cluster in self.clusters:
            e = 0.0
            for topic, docs in self.bible.topics.items():
                p = len(set(cluster.docs).intersection(docs)) / float(len(docs))
                if p > 0.0:
                    e += p * math.log(p, 2) * -1
            sum += len(cluster.docs) * e
        
        return sum / Doc.count
    
    def fmeasure(self):
        """
        Calculates the F-measure for this cluster solution.
        """
        num = 0.0
        for topic, docs in self.bible.topics.items():
            max_f = None
            for cluster in self.clusters:
                n = len(set(cluster.docs).intersection(docs)) / float(len(docs))
                recall = n / float(len(docs))
                precision = n / float(len(cluster.docs))
                if recall != 0.0 or precision != 0.0:
                    f = (2 * precision * recall) / (precision + recall)
                else:
                    f = 0.0
                
                max_f = max(f, max_f)
            
            num += len(docs) * max_f
        
        return num / Doc.count
    
    def evaluate(self):
        """
        Returns the evaluation for this clustering solution.
        """
        return str(self.entropy()) + "\t" + \
                str(self.fmeasure()) + "\t" + \
                str(self.similarity()) + "\t" + \
                str(self.silhouette())
        
    # ABSTRACT
    def execute(self, docs):
        """
        Main execution.
        
        Key arguments:
        docs -- the documents to cluster.
        """
        pass
    
    def results(self, result_file):
        """
        Save the results to a file.
        
        Key arguments:
        result_file -- file to output to.
        """
        # Inverse the bible.
        ibible = dict((v.index, k) for k, v in self.bible.words.iteritems())
        
        result_handle = open(result_file, 'w')
        
        output = ""
        
        i = 1
        for cluster in self.clusters:
            output += "Cluster " + str(i) + "\n\n"
            
            # Documents in ths cluster
            output += "\tDocuments:\n"
            j = 1
            for doc in cluster.docs:
                output += "\t\t" + str(j) + ". " + str(doc.id) + "\n"
                j += 1
            
            # Find top 3 words.
            output += "\n\tTop Words:\n"
            indices = sorted(cluster.centroid, key=cluster.centroid.get, reverse=True)[:3]
            j = 1
            for index in indices:
                output += "\t\t" + str(j) + ". " + str(ibible[index]) + "\n"
                j += 1
            
            output += "\n\n"
            i += 1
        
        result_handle.write(output)
        result_handle.close()
    
    def silhouette(self):
        """
        Find the *average* silhouette coefficient for the cluster solution.
        """
        sil = 0.0
             
        for doc in self.bible.docs:
            # Calculate a.
            a = 0.0
            for doc2 in doc.cluster.docs:
                if doc != doc2:
                    a += self.cosine(doc.tfidf, doc2.tfidf)
            a /= len(doc.cluster.docs)
            
            # Calculate b.
            b = 0.0
            max_b = 0.0
            
            for cluster in self.clusters:
                if doc.cluster != cluster:
                    for doc2 in cluster.docs:
                        b = self.cosine(doc.tfidf, doc2.cluster.centroid)
                        if b > max_b:
                            max_b = b
            
            sil += (a - max_b) / max(a, max_b)
        
        return sil / Doc.count
            
    def similarity(self):
        """
        Find the *average* similarity of the clusters.
        """
        sim = 0.0
        for cluster in self.clusters:
            for index, value in cluster.centroid.items():
                sim += value * value
        
        return sim / len(self.clusters)