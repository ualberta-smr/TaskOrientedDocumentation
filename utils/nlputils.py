VERB_IDENTIFIERS = ['VB', 'VBD', 'VBG', 'VBN', 'VBZ'] #excluding VBP becuase it refers to personal verbs
NOUN_IDENTIFIERS = ['NN', 'NNS', 'NNP', 'NNPS']
ADJ_IDENTIFIERS = ['JJ', 'JJR', 'JJS']


PATTERNS_LIST = [
    'dobj', 'prep', 'case', 'nsubjpass', 'nmod', 'neg', 'prt', 'nn', 'amod',
]

PATTERNS = {
    'dobj': ['dobj'],
    'prep': ['prep'],
    'agent': ['case'],
    'nsubjpass': ['nsubjpass'],
    'rcmod': ['nmod'],
    'neg': ['neg'],
    'prt': ['prt'],
    'nn': ['nn'],
    'amod': ['amod'],
}
