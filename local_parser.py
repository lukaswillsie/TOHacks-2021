import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from IPython.display import display
from stat_parser import Parser

synonym_dict = {
    'add' : ('plus'),
    'subtract' : ('minus'),
    'multiply' : ('product'),
    'divide' : (),
    'power' : ('exponentiate'),
    'about' : ('regarding', 'concerning'),
    'summarize' : ('summarise'),
    'translate' : ()
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
        for word in self.parsed_text:
            for ops in self.ops:
                if self.equals(ops, word[0]):
                    self.verb = [ops]
                    return [ops]
        return self.extract_verb_math()

    def collect_args_math(self):
        res = []
        for j in range(len(self.verb_ranges) - 1):
            res.append(self.collect_args_math_helper(self.verb_ranges[j] + 1, self.verb_ranges[j + 1]))
        res.append(self.collect_args_math_helper(self.verb_ranges[-1], len(self.parsed_text)))
        return res

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
            if 'TO' in temp:
                res.append(range(vals[i], vals[i + 1] + 1))
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
        else:
            return self.collect_args_math()

    def equals(self, word1, word2):
        return word2 in self.get_synonyms(word1) or word1 in self.get_synonyms(word2) or word1.lower() == word2.lower() \
            or word2 in synonym_dict[word1]

    def get_synonyms(self, word):
        s = set()
        for ss in wordnet.synsets(word):
            for wordz in ss.lemma_names():
                s.add(wordz)
        return s



if __name__ == "__main__":
    text = "add 7 and 8 multiply by 6"
    custom_sent_tokenizer = PunktSentenceTokenizer(text)
    tokenized = custom_sent_tokenizer.tokenize(text)
    words = nltk.word_tokenize(tokenized[0])
    tagged = nltk.pos_tag(words)
    print(tagged)
    parser = TextParser(text)
    print(parser.get_synonyms('about'))
    print(parser.extract_verb())
    print(parser.collect_args())
