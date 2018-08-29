import csv
import pdb
from pyquery import PyQuery


#list of words related to API quality
QUALITY_WORDS = [
"integrity", "security", "interoperability", "testability", "maintainability",  "traceability",  "accuracy",  "modifiability",  "understandability", "availability", "modularity", "usability", "correctness", "performance",  "verifiability",  "efficiency", "portability", "flexibility,reliability", "testability", "changeability", "analyzability", "stability", "maintain", "maintainable", "modularity", "modifiability", "understandability", "interdependent", "dependency", "encapsulation", "decentralized", "modular", "security", "compliance", "accuracy", "interoperability", "suitability", "functional", "practicality", "functionality", "compliant", "exploit", "certificatesecured", "buffer", "overflow", "policy", "malicious", "trustworthy", "vulnerable", "vulnerability", "accurate", "secure", "vulnerability", "correctness", "accuracy", "conformance", "adaptability", "replaceability", "installability", "portable", "movableness", "movability", "portability", "specification", "migration", "standardized", "l10n", "localization", "i18n", "internationalization", "documentation", "interoperability", "transferability", "resource", "behaviour", "time", "behaviour", "efficient", "efficiency", "performance", "profiled", "optimize", "sluggish", "factor", "penalty", "slower", "fasterslow", "fast", "optimization", "operability", "understandability", "learnability", "useable", "usable", "serviceable", "usefulness", "utility", "useableness", "usableness", "serviceableness", "serviceability", "usability", "gui", "accessibility", "menu", "configure", "convention", "standard", "feature", "focus", "ui", "mouse", "icons", "ugly", "dialog", "guidelines", "click", "default", "human", "convention", "friendly", "user", "screen", "interface", "flexibility", "fault", "tolerance", "recoverability", "maturity", "reliable", "dependable", "responsibleness", "responsibility", "reliableness", "reliability", "dependableness", "dependability", "resilience", "integrity", "stability", "stable", "crashbug", "fails", "redundancy", "error", "failure"
]


#list of stop words", 
STOP_WORDS = [
    "a", 
    "about", 
    "above", 
    "after", 
    "again", 
    "against", 
    "all", 
    "am", 
    "an", 
    "and", 
    "any", 
    "are", 
    "aren't", 
    "as", 
    "at", 
    "be", 
    "because", 
    "been", 
    "before", 
    "being", 
    "below", 
    "between", 
    "both", 
    "but", 
    "by", 
    "can't", 
    "cannot", 
    "could", 
    "couldn't", 
    "did", 
    "didn't", 
    "do", 
    "does", 
    "doesn't", 
    "doing", 
    "don't", 
    "down", 
    "during", 
    "each", 
    "few", 
    "for", 
    "from", 
    "further", 
    "had", 
    "hadn't", 
    "has", 
    "hasn't", 
    "have", 
    "haven't", 
    "having", 
    "he", 
    "he'd", 
    "he'll", 
    "he's", 
    "her", 
    "here", 
    "here's", 
    "hers", 
    "herself", 
    "him", 
    "himself", 
    "his", 
    "how", 
    "how's", 
    "i", 
    "i'd", 
    "i'll", 
    "i'm", 
    "i've", 
    "if", 
    "in", 
    "into", 
    "is", 
    "isn't", 
    "it", 
    "it's", 
    "its", 
    "itself", 
    "let's", 
    "me", 
    "more", 
    "most", 
    "mustn't", 
    "my", 
    "myself", 
    "no", 
    "nor", 
    "not", 
    "of", 
    "off", 
    "on", 
    "once", 
    "only", 
    "or", 
    "other", 
    "ought", 
    "our", 
    "ours",
    "ourselves", 
    "out", 
    "over", 
    "own", 
    "same", 
    "shan't", 
    "she", 
    "she'd", 
    "she'll", 
    "she's", 
    "should", 
    "shouldn't", 
    "so", 
    "some", 
    "such", 
    "than", 
    "that", 
    "that's", 
    "the", 
    "their", 
    "theirs", 
    "them", 
    "themselves", 
    "then", 
    "there", 
    "there's", 
    "these", 
    "they", 
    "they'd", 
    "they'll", 
    "they're", 
    "they've", 
    "this", 
    "those", 
    "through", 
    "to", 
    "too", 
    "under", 
    "until", 
    "up", 
    "very", 
    "was", 
    "wasn't", 
    "we", 
    "we'd", 
    "we'll", 
    "we're", 
    "we've", 
    "were", 
    "weren't", 
    "what", 
    "what's", 
    "when", 
    "when's", 
    "where", 
    "where's", 
    "which", 
    "while", 
    "who", 
    "who's", 
    "whom", 
    "why", 
    "why's", 
    "with", 
    "won't", 
    "would", 
    "wouldn't", 
    "you", 
    "you'd", 
    "you'll", 
    "you're", 
    "you've", 
    "your", 
    "yours", 
    "yourself", 
    "yourselves"
]


PUNCTUATION = ["!", ".", ",", "?", "(", ")", "[", "]", "{", "}", ":", ";", "-"]


INPUT_FILE = 'data/testng.csv'
OUTPUT_FILE = 'output/output.txt'
SUPERVISED_INPUT_FILE = 'output/titles-200.txt'

def get_questions():
    questions = []
    with open(INPUT_FILE, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            questions.append(row)

    return questions[1:]

def get_qtitles():
    question_titles = []
    with open(INPUT_FILE, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            question_titles.append(row[1].lower())

    question_titles.pop(0)

    return question_titles


def supervised_qtitles():
    supervised_titles = []
    with open(SUPERVISED_INPUT_FILE, mode='r') as infile:
        lines = infile.readlines()
        for line in lines:
            label = line[0]
            text = line[2:]

            if not text[len(text) - 1] in '?!.;':
                text = text + "?"

            supervised_titles.append({
                    "text": text,
                    "label": label
                })

    return supervised_titles



def lower_text(line):
    tokens = line.split()
    res = []
    for i, word in enumerate(tokens):
        if i == 0:
            res.append(word)

        else:
            first_let = word[0].lower()
            res.append(first_let + word[1:])

    res_str = ""
    for item in res:
        res_str = res_str + " " + item

    return res_str.strip()


class Tokenizer:
    def tokenize(sentence):
        #remove all punctuation and whitespace around the text
        temp = sentence

        for item in PUNCTUATION:
            temp = temp.replace(item, "")


        tokens = temp.split(" ")
        tokens_list = []
        for token in tokens:
            token = token.replace(" ", "")
            if not token == "":
                tokens_list.append(token)

        return tokens


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

    def tokenize_code(html):
        res = []
        pq = PyQuery(html)

        snippets = pq.children("pre code")
        for snippet in snippets:
            res.append(snippet.text)

        return res






#'<pre><code>int foo = Integer.parseInt("1234");\n</code></pre>\n\n<p>See the <a href="http://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html#parseInt-java.lang.String-" rel="noreferrer">Java Documentation</a> for more information.</p>\n\n<p><em>(If you have it in a <code>StringBuilder</code> (or the ancient <code>StringBuffer</code>), you\'ll need to do <code>Integer.parseInt(myBuilderOrBuffer.toString());</code> instead).</em></p>\n'
