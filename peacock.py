import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet

from IPython.display import display

from stat_parser import Parser


for ss in wordnet.synsets('sum'):
    print(ss.name(), ss.lemma_names())

parser = Parser()
print(parser.parse("Find the sum from 1 to 100"))
