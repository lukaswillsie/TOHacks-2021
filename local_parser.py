import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from stat_parser import Parser
import math
from math import sqrt
from itertools import count, islice

synonym_dict = {
    'add' : ('plus',),
    'subtract' : ('minus',),
    'multiply' : ('product',),
    'divide' : (),
    'power' : ('exponentiate',),
    'about' : ('regarding', 'concerning'),
    'summarize' : ('summarise',),
    'translate' : (),
    'question' : ()
    }

anti_synonym_dict = {
    'add' : (),
    'subtract' : (),
    'multiply' : (),
    'divide' : (),
    'power' : (),
    'about' : (),
    'summarize' : ('sum',),
    'translate' : (),
    'question' : ()
}

class TextParser:

    def __init__(self, text):
        parser = Parser()
        self.math_ops = (
            'add',
            'multiply',
            'divide',
            'subtract',
            'power'
        )
        self.ops = (
            'summarize',
            'translate'
        )
        custom_sent_tokenizer = PunktSentenceTokenizer(text)
        tokenized = custom_sent_tokenizer.tokenize(text)
        words = nltk.word_tokenize(tokenized[0])
        self.parsed_text = nltk.pos_tag(words)
        self.verb = []
        self.verb_ranges = []
        self.language = ''
        self.keywords = ['odd', 'even', 'prime', 'composite', 'square', 'cube']
        self.special = sum([word[0] in self.keywords for word in self.parsed_text]) > 0
        self.special_keywords = set()
        for word in self.parsed_text:
            if word[0] in self.keywords:
                self.special_keywords.add(word[0])
        self.special_keywords = list(self.special_keywords)
        self.d = d = {
            "odd": lambda x: x% 2 == 1,
            "even": lambda x: x% 2 == 0,
            "square": lambda x: math.sqrt(x).is_integer(),
            "cube":lambda x: (x**(1./3.)).is_integer(),
            "prime": lambda x: x > 1 and all(x % i for i in islice(count(2), int(sqrt(x)-1))),
            "composite": lambda x: x > 1 and not all(x % i for i in islice(count(2), int(sqrt(x)-1)))
        }
        

    def extract_verb_math(self):
        ids = []
        verbs = []
        for i in range(len(self.parsed_text)):
            word = self.parsed_text[i]
            if 'N' in word[1] or 'V' in word[1] or "R" in word[1] or "J" in word[1]:
                for ops in self.math_ops:
                    if self.equals(ops, word[0]):
                        verbs.append(ops)
                        ids.append(i)
            try:
                temp = [self.parsed_text[j][1] for j in range(i,i+3)]
            except:
                temp = []
            if temp == ['IN', 'DT', 'NN']:
                for ops in self.math_ops:
                    if self.equals(ops, self.parsed_text[i + 2][0]):
                        verbs.append(ops)
                        ids.append(i)
        if len(ids) == 0:
            return None
        else:
            self.verb_ranges = ids
            self.verb = verbs
            return self.verb
    
    def extract_verb_summary(self):
        self.verb = 'summarize'
        return ['summarize']
    
    def extract_verb(self):
        temp = self.get_synonyms('summarize').union(self.get_synonyms('find'))
        if self.parsed_text[0][0].lower() in ['who', 'where', 'when', 'why', 'how']:
            self.verb = ['question']
            return ['question'] 
        for word in self.parsed_text:
            for ops in self.ops:
                if self.equals(ops, word[0]):
                    self.verb = [ops]
                    return [ops]
        for word in self.parsed_text:
            for ops in self.math_ops:
                if self.equals(ops, word[0]):
                    return self.extract_verb_math()
        self.verb = ['question']
        return ['question']

    def collect_args_math(self):
        res = []
        for j in range(len(self.verb_ranges) - 1):
            res.append(self.collect_args_math_helper(self.verb_ranges[j] + 1, self.verb_ranges[j + 1]))
        res.append(self.collect_args_math_helper(self.verb_ranges[-1], len(self.parsed_text)))
        return res
    
    def special_range(self, r, keywords):
        return_lst = []
        for i in r:
            add = True
            for keyword in keywords:
                if not self.d[keyword](i):
                    add = False
            if add:
                return_lst.append(i)
        return return_lst

    def collect_args_math_helper(self, start, end):
        idx = []
        vals = []
        res = []
        for i in range(start, end):
            if self.parsed_text[i][1] == 'CD':
                idx.append(i)
                vals.append(int(self.parsed_text[i][0]))
        i = 0
        while i < len(idx):
            if i < len(idx) - 1:
                temp = [self.parsed_text[j][1] for j in range(idx[i], idx[i + 1])]
            else:
                temp = []
            if 'TO' in temp and ('from' in self.parsed_text[idx[i] - 1][0] or 'between' in self.parsed_text[idx[i] - 1][0]):
                ran = range(min(vals[i], vals[i + 1]), max(vals[i], vals[i + 1]) + 1)
                if self.special:
                    res.extend(self.special_range(ran, self.special_keywords))
                else:
                    res.append(ran)
                i += 1
            else:
                res.append(vals[i]) 
            i += 1
        return res
    
    def collect_args_summary(self):
        temp = [item[0] for item in self.parsed_text]
        idx = max(loc for loc, val in enumerate(temp) if self.equals('about', val))
        temp_res = self.parsed_text[idx+1:]
        res = []
        s = ''
        for entry in temp_res:
            if 'and' not in entry[0]:
                s += entry[0] + ' '
            else:
                res.append(s.strip())
                s = ''
        if s != '':
            res.append(s.strip())
        return res
    
    def collect_args_translate(self):
        temp = [item[0] for item in self.parsed_text]
        languages = ['english', 'french', 'spanish', 'korean', 'russian']
        for word in self.parsed_text:
            if word[0] in languages:
                language = word[0]
                self.language = language
        idx = max(loc for loc, val in enumerate(temp) if val == language)
        return " ".join(temp[idx + 1:])
    
    def collect_args(self):
        if self.verb[0] == 'summarize':
            return self.collect_args_summary()
        elif self.verb[0] == 'translate':
            return self.collect_args_translate()
        elif self.verb[0] == 'question':
            return " ".join([word[0] for word in self.parsed_text])
        else:
            return self.collect_args_math()

    def equals(self, word1, word2):

        return (word2 in self.get_synonyms(word1) or word1 in self.get_synonyms(word2) or word1.lower() == word2.lower() \
            or word2 in synonym_dict[word1]) and word2 not in anti_synonym_dict[word1]

    def get_synonyms(self, word):
        s = set()
        for ss in wordnet.synsets(word):
            for wordz in ss.lemma_names():
                s.add(wordz)
        return s



if __name__ == "__main__":
    text = "sum of all the odd and prime numbers from 1 to 100"
    custom_sent_tokenizer = PunktSentenceTokenizer(text)
    tokenized = custom_sent_tokenizer.tokenize(text)
    words = nltk.word_tokenize(tokenized[0])
    tagged = nltk.pos_tag(words)
    print(tagged)
    parser = TextParser(text)
    print(parser.equals('summarize', 'is'))
    print('summarize: ', parser.get_synonyms('summarize'))
    print('is: ', parser.get_synonyms('is'))
    print(parser.extract_verb())
    print(parser.special_keywords)
    print(parser.collect_args())
