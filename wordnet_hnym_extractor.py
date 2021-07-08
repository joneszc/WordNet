# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 16:07:47 2021

@author: joneszc
"""
import re
import string as s
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
#from nltk.stem.snowball import SnowballStemmer
#stemmer = SnowballStemmer('english')

def preprocess_string(string):
    '''Ingest string, replace punctuation and whitespace with single space,
    remove extra spaces, lemmatize, and finally lowercase the string'''
    table = str.maketrans({key: ' ' for key in s.punctuation+s.whitespace}) 
    new_string = re.sub(' +',' ',string.translate(table)).strip()
    tokens=[' '.join([wordnet_lemmatizer.lemmatize(w) for w in new_string.split(' ')])]
    #tokens=[' '.join([wordnet_lemmatizer.lemmatize(stemmer.stem(w)) for w in new_string.split(' ')])]
    new_string = ' '.join(tokens).lower().strip()
    return new_string

def get_permutations(inputText):
    '''Slice string into all possible permutations, retaining word-order, 
    to account for all possible phrases discoverable in string, linked w/ underscores'''
    l = inputText.lower().strip().split()
    permutationsList=[]
    for i in range(len(l)):
        #print(l[:i])
        ngrams = zip(*[l[i:]]) # Add permutations counting from left
        permutationsList.append([x[0] for x in ngrams])
        ngrams2 = zip(*[l[:i]]) # Add permutations counting from right
        permutationsList.append([x[0] for x in ngrams2]) 
        permutationsList.append(l[i:len(l)-i]) # Add permutations accross the middle
        permutationsList.append(l[i:i+2]) # Add pairs moving left-to-right
    return sorted(list(set(['_'.join(ele) for ele in permutationsList if len(ele)>1])), key=len, reverse=True)

def get_phrases(inputText):
    '''iterate through permutations of elements in input string attached by underscores
    and check for matches in wordnet; output matches as detected phrases from input'''
    phrases = list(set(get_permutations(inputText)+get_permutations(preprocess_string(inputText))))
    phrase_matches = list(filter(lambda x: wn.synsets(x)!=[], phrases))
    return phrase_matches

def get_tokens(inputText):
    '''Convert input string into tokens--split string on spaces--then augment list
    with preprocessed tokens to optimize results'''
    tokens = list(set(inputText.lower().strip().split() + preprocess_string(inputText).split()))
    #tokens = list(filter(lambda x: wn.synsets(x)!=[], tokens))
    return tokens

def get_synset_match(synset, hyponyms=True):
    '''Query wordnet with sysnset terms for hyponyms or hypernyms and
    return results separated by commas'''
    if hyponyms == True:
        holder=', '.join([h.name() for h in wn.synset(synset).hyponyms()])
    else:
        holder=', '.join([h.name() for h in wn.synset(synset).hypernyms()])
    if holder!='':
        return holder
    else:
        pass

def get_hypernyms(tokens):
    '''Use dictionary comprehension to obtain all hypernyms using NLTK wordnet sysnet module'''
    hypernyms_dict = {w: list(filter(lambda x: x!=None,[get_synset_match(i,hyponyms=False) for i in [x.name() for x in wn.synsets(w)]])) for w in tokens}
    return hypernyms_dict

def get_hyponyms(tokens):
    '''Use dictionary comprehension to obtain all hyponyms using NLTK wordnet sysnet module'''
    hyponyms_dict = {w: list(filter(lambda x: x!=None,[get_synset_match(i) for i in [x.name() for x in wn.synsets(w)]])) for w in tokens}
    return hyponyms_dict

def get_results(inputText):
    '''Extract all hypernyms and hyponyms from string and output results into a list of
    dictionaries with both hypernyms and hyponyms as keys and their values in alphabetical order'''
    hypos = set()
    hypers = set()
    result_list = []
    tokens = get_tokens(inputText)+get_phrases(inputText)
    hyponyms = get_hyponyms(tokens)
    hypernyms = get_hypernyms(tokens)
    for i in sorted(tokens, key=len, reverse=True):
        print(str(i+"\n"+"Hyponyms: "+str(hyponyms[i])+"\n"+"Hypernyms: "+str(hypernyms[i])+"\n"))
        for ele in hyponyms[i]:
            hypos.add(ele)
        for ele in hypernyms[i]:
            hypers.add(ele)   
    result_list.append({'hyponyms': sorted(list(hypos))})
    result_list.append({'hypernyms': sorted(list(hypers))})
    return list(result_list)
    

# Print and return list of all hyponyms and hypernyms of WordNet-matched terms & phrases in input text:
if __name__ == "__main__":
    
    inputText = '''\tThe differential diagnosis of multiple myeloma usually involves the
    spectrum of plasma cell proliferative disorders shown in Table
    3.1,2,6,13,14,20 A full evaluation will help classify where a patient
    falls in this spectrum.\n The differential diagnosis of bone lesions
    includes primary or metastatic cancer, benign bone lesions,
    osteoporotic compression fracture, and other bone conditions.21,22 The
    full differential diagnosis for patients presenting with fatigue,
    unexplained weight loss, or hypercalcemia is broad and beyond the
    scope of this article.23-25'''
    
    hyponyms_and_hypernyms = get_results(inputText)
