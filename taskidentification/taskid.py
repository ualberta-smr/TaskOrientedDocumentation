import re
import pdb


from pyquery import PyQuery
from utils.fileutils import Tokenizer
from api.seapi import answers_to_question
from taskidentification.regex import CODE_ELEMENTS_REGEX as REGEX
from taskidentification.similarity import STOP_all_words, PUNCTUATION
from utils.nlputils import VERB_IDENTIFIERS, NOUN_IDENTIFIERS, ADJ_IDENTIFIERS, PATTERNS_LIST



def tokenize_HTML(html):
    sentences = ""
    pq = PyQuery(html)
    p_s = pq.children("p").items()
    for p in p_s:
        sentences = sentences + p.text() + " "

    flag = False
    adj_words = []

    for word in QUALITY_WORDS:
        if word in sentences:
            flag = True
            adj_words.append(word)

    if flag:
        pass
        #print(sentences + "\t" + adj_words.__str__())
                
    return sentences    


class SentenceParser(object):

    index = {
        'id': 0,
        'title': 1,
        'body': 2,
        'tags': 3,
        'accepted_id': 4,
    }

    def __init__(self, link, question_dict, corenlp):

        index = SentenceParser.index

        #initialize object information
        self.sentence = question_dict["title"]
        self.id = link
        self.body = question_dict["body"]
        self.tags_str = question_dict["tags"]
        self.corenlp = corenlp

        #store the tags associated with the question
        self.parse_tags()

        #annotate text using the CoreNLP library.
        annotated_text = corenlp.annotate(self.sentence, properties = {
            #list of all annotators: tokenize,ssplit,pos,depparse,parse
            'annotators': 'depparse,pos',
            'outputFormat': 'json'
        })
        self.annotated_text = annotated_text['sentences'][0]

        #get best answer to this question
        # self.best_answer = self.get_best_answer()


    def parse_tags(self):
        #if it's exactly one tag return that one tag
        if self.tags_str.count("<") == 1:
            return [self.tags_str[1:len(self.tags_str) - 2], ]

        #if it's more than one tags
        raw_list = self.tags_str.split("><")
        res = []
        for item in raw_list:
            temp = item.replace("<", "").replace(">", "")
            res.append(temp)

        self.tags_list = res




    def is_task(self):
        #this function returns a boolean value that shows whether the tokens passed represent a task or not
        isa_task = False
        has_verb = False
        for item in self.annotated_text['tokens']:
            if item['pos'] in VERB_IDENTIFIERS:
                has_verb = True
                break

        tokens = self.annotated_text['basicDependencies']

        for pattern in PATTERNS_LIST:
            if SentenceParser.match(tokens, pattern):
                isa_task = True

        return isa_task


    def get_task(self):
        #this function returns a string representing the task referred to in the annotated_text
        task = []

        tokens = self.annotated_text['tokens']
        #the previous method of task extraction that extracted word with certain grammatical
        #roles in the sentence appended them as the task
        for i, token in enumerate(tokens):
            if token['pos'] in VERB_IDENTIFIERS:
                task.append(token['word'])
            elif token['pos'] in NOUN_IDENTIFIERS:
                task.append(token['word'])
            elif token['pos'] == 'IN':
                task.append(token['word'])
            elif token['pos'] == 'TO' and not tokens[i-1]['pos'] == "WRB": #If it's a "how to" sentence, we want to ignore the
                                                                            #"How to" part.
                task.append(token['word'])
        task_str = ""
        for item in task:
            task_str = task_str + item.__str__() + " "

        return task_str


    def get_target_API(self):

        matches = SentenceParser.match_regex(self.best_answer.body)

        freqs = {} 

        for match in matches: 
            if freqs.get(match, None): 
                freqs[match] += 1
            else: 
                freqs[match] = 1


        freqs = {key: value for key, value in freqs.items() if not value < 5 and not len(key) < 4 and not key.lower() in ['code', 'pre', 'html', 'java']}


        # for key, value in freqs.items(): 
        #     if len(key) <= 3: 
        #         freqs.pop(key, 0)
        #     elif value < 5: 
        #         freqs.pop(key, 0)

        return freqs


        # code_snippets = self.query('code')
        # snippet_tags = self.query('pre code')
        # code_words = []

        # for item in code_snippets:
        #     if item not in snippet_tags:
        #         code_words.append(item)

        # return code_words



    def get_best_answer(self):
        #print("Calling best answer with " + self.id.__str__())
        answers = answers_to_question(self.id)
        self.answers = answers
        best_answer = None

        max_votes = -1
        for answer in answers:
            if answer.score > max_votes:
                best_answer = answer
                max_votes = answer.score

        self.best_answer = best_answer

        return best_answer


    # def get_solution_code(self):
    #     snippet_tags = self.query('pre code')



    def get_annotated_answer(self):
        self.clean_answer_body()
        annotated = self.corenlp.annotate(self.parsed_answer, properties = {
            'annotators': 'pos',
            'outputFormat': 'json'
        })

        return annotated


    def clean_answer_body(self):
        #HTML parser for answer text
        parsed_answer = Tokenizer.tokenize_HTML(self.best_answer.body)
        self.parsed_answer = parsed_answer



    def match(tokens, pats):

        matches = False

        for token in tokens:
            if token['dep'] == pats:
                matches = True


        return matches

    @staticmethod
    def match_regex(string):
        res = []

        for regex in REGEX:
            p = re.compile(regex)
            matched = p.findall(string)
            if matched:
                for match in matched:
                    match_str = None
                    if type(match) == str:
                        match_str = match
                    else:
                        match_str = match[0]

                    words = re.findall(r"[\w']+", match_str)

                    for word in words: 
                        res.append(word)

        return res
