# WordNet-string-parser
Uses NLTK to extract hyponyms and hypernyms for words and phrases mapped in WordNet from an input string. 
The string is broken into iterations of permutations for pairing underscore-linked chunks of text with phrases matched in WordNet.
A pre-processing step creates a new version of the string that is optimized for WordNet performance with stemming and elimination of punctuation.
Both the pre-processed string and original string are tokenized and matches with WordNet are returned, after removal of duplicates using set().
All hyponyms and hypernyms are returned for detected WordNet synset matches from the tokenized string.
