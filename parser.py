import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from IPython.display import display
from stat_parser import Parser


class TextParser:

    def __init__(self, text):
        parser = Parser()
        self.math_ops = (
            'add',
            'multiply',
            'divide',
            'subtract'
        )
        custom_sent_tokenizer = PunktSentenceTokenizer(text)
        tokenized = custom_sent_tokenizer.tokenize(text)
        words = nltk.word_tokenize(tokenized[0])
        self.parsed_text = nltk.pos_tag(words)
        self.verb = ''
        self.args = []

    def extract_verb_math(self):
        for i in range(len(self.parsed_text)):
            word = self.parsed_text[i]
            if 'N' in word[1] or 'V' in word[1]:
                for ops in self.math_ops:
                    if self.equals(ops, word[0]):
                        self.verb = ops
                        return True
            temp = [self.parsed_text[j][1] for j in range(i,i+3)]
            if temp == ['IN', 'DT', 'NN']:
                for ops in self.math_ops:
                    if self.equals(ops, self.parsed_text[i + 2][0]):
                        self.verb = ops
                        return True
        return False
            
    def collect_args_math(self):
        idx = []
        vals = []
        res = []
        for i in range(len(self.parsed_text)):
            if self.parsed_text[i][1] == 'CD':
                idx.append(i)
                vals.append(int(self.parsed_text[i][0]))
        i = 0
        while i < len(idx):
            if i < len(idx) - 1:
                temp = [self.parsed_text[j][1] for j in range(idx[i], idx[i + 1])]
            else:
                temp = []
            if 'TO' in temp:
                res.append(range(vals[i], vals[i + 1] + 1))
                i += 1
            else:
                res.append(vals[i])
            i += 1
        self.args = res
        return res

    def equals(self, word1, word2):
        return word2 in self.get_synonyms(word1) or word1 in self.get_synonyms(word2)
    
    def get_synonyms(self, word):
        s = set()
        for ss in wordnet.synsets(word):
            for wordz in ss.lemma_names():
                s.add(wordz)
        return s



if __name__ == "__main__":
    text = "Multiply the numbers from 1 and 15"
    # custom_sent_tokenizer = PunktSentenceTokenizer(text)
    # tokenized = custom_sent_tokenizer.tokenize(text)
    # words = nltk.word_tokenize(tokenized[0])
    # tagged = nltk.pos_tag(words)
    # print(tagged)
    parser = TextParser(text)
    print(parser.extract_verb_math())
    print(parser.collect_args_math())
    print(parser.verb)
