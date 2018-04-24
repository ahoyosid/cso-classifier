#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 15:16:13 2018

@author: angelosalatino
"""
   
def load_cso(file):
    import csv
    with open(file) as ontoFile:
        topics = {}
        parents = {}
        same_as = {}
        ontology=csv.reader(ontoFile, delimiter=';')
        for triple in ontology:
            if(triple[1] == 'klink:broaderGeneric'):
                if(triple[2] in parents):
                    parents[triple[2]].append(triple[0])
                else:
                    parents[triple[2]] = [triple[0]]
            elif(triple[1] == 'klink:relatedEquivalent'):
                if(triple[2] in same_as):
                    same_as[triple[2]].append(triple[0])
                else:
                    same_as[triple[2]] = [triple[0]]
            elif(triple[1] == 'rdfs:label'):
                topics[triple[0]] = True
                
    cso = {'topics':topics, 'parents':parents, 'same_as':same_as}
            
    return(cso)
        
        

def cso_matcher(paper, cso, format="text", num_siblings=2):
    from nltk import ngrams
    from nltk.tokenize import word_tokenize
    from nltk.tokenize import RegexpTokenizer
    from nltk.corpus import stopwords
    
    """
    Given a paper it returns the topics.
    paper = paper
    format = ['text','json']
    
    return the topics found in the text (found_topics)
    """
    if(format == 'json'):
        t_paper = paper
        paper = ""
        for key in list(t_paper.keys()):
            paper = paper + t_paper[key] + " "
            
            
    
    """ preprocessing
    """    
    paper = paper.lower()
    tokenizer = RegexpTokenizer(r'[\w\-\(\)]*')
    tokens = tokenizer.tokenize(paper)
    filtered_words = [w for w in tokens if not w in stopwords.words('english')]
    paper =  " ".join(filtered_words)
    
    
    """ analysing grams
    """
    found_topics=[]
    
    word_list = paper.split(" ")
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    
    word = ngrams(word_tokenize(paper,preserve_line=True), 1)
    for grams in word:
      if(word in cso['topics']):
            found_topics.append(word) 

    bigrams = ngrams(word_tokenize(paper,preserve_line=True), 2)
    for grams in bigrams:
        if(" ".join(grams) in cso['topics']):
            found_topics.append(" ".join(grams)) 
      
    trigrams = ngrams(word_tokenize(paper,preserve_line=True), 3)
    for grams in trigrams:
        if(" ".join(grams) in cso['topics']):
            found_topics.append(" ".join(grams)) 
            
    """ analysing similarity
    """
    found_topics = statistic_similarity(found_topics)
    
    """ extract more concepts from the ontology
    """
    found_topics = climb_ontology(found_topics,cso,num_siblings=num_siblings)

    return (found_topics)



def climb_ontology(found_topics,cso,num_siblings=2):
    from itertools import combinations
    combinations = combinations(range(len(found_topics)), num_siblings) # generates all possible combinations
    for combination in combinations:
        all_parents = {}
        for val in combination:
            parents = cso['parents'][found_topics[val]]
            for parent in parents:
                if(parent in all_parents):
                    ++all_parents[parent]
                else:
                    all_parents[parent] = 1
        for parent, times in all_parents.items():    
            if(times == num_siblings):
                if(parent not in found_topics):
                    found_topics.append(parent)
        all_parents.clear()
            
    return (found_topics)

def statistic_similarity(paper):
    return (paper)