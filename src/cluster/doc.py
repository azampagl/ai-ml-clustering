"""
Document object.

@author Aaron Zampaglione <azampagl@my.fit.edu>
@course CSE 5800 Advanced Topics in CS: Learning/Mining and the Internet, Fall 2011
@project Proj 03, CLUSTERING
@copyright Copyright (c) 2011 Aaron Zampaglione
@license MIT
"""
from lib.dotdict import dotdict

import math

class Doc(object):
    """
    Document object for all clustering algorithms.
    """
    # Static count variable.
    count = 0
    
    @classmethod
    def factory(cls, topic, id, words, bible):
        doc = Doc()
        
        doc.topic = topic
        doc.id = id
        doc.words = {}
        
        for word in words:
            # Update the bible.
            if not word in bible.words:
                bible.words[word] = dotdict()
                bible.words[word].index = len(bible.words) - 1
                bible.words[word].docs = [doc]
            else:
                if not doc in bible.words[word].docs:
                    bible.words[word].docs.append(doc)
            
            # Update this doc.
            if word in doc.words:
                doc.words[word] += 1
            else:
                doc.words[word] = 1
        
        # Increment the number of documents processed.
        Doc.count += 1
        
        # No cluster yet!
        doc.cluster = None
        
        return doc
    
    # Document id.
    id = ''
    
    # Words in this document.
    words = {}
    
    # TF-IDF vector.
    tfidf = {}
    
    # What cluster this doc belongs to.
    cluster = None
    
    def __str__(self):
        """
        Converts the document to a string.
        """
        output = str(self.id) + "\n"
        output += str(self.topic) + "\n"
        output += " ".join(map(str, self.tfidf.values())) + "\n\n"
        return output
    
    def init(self, bible):
        """
        Calculate the TFIDF for this document.
        
        Key arguments:
        bible -- global word dictionary
        """
        self.tfidf = {}
        
        words_len = float(len(self.words))
        
        mag = 0.0
        for word, meta in bible.words.items():
            if word in self.words:
                # Term frequency.
                tf = self.words[word] / words_len
                # Inverse document frequency.
                idf = math.log(Doc.count / float(len(meta.docs)), 2)
                
                tfidf = tf * idf
                
                self.tfidf[meta.index] = tfidf
                mag += tfidf * tfidf
            else:
                self.tfidf[meta.index] = 0.0
        
        mag = math.sqrt(mag)
        
        for index in self.tfidf:
            self.tfidf[index] /= mag