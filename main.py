#!/usr/bin/env python3


#self defined packages
#from utils.serializer import serialize_task
from taskidentification.taskid import SentenceParser
from taskidentification.similarity import get_similar_tasks, shingling
from utils.nlputils import VERB_IDENTIFIERS, NOUN_IDENTIFIERS
from taskidentification.similarity import STOP_all_words, PUNCTUATION
from utils.fileutils import get_qtitles, supervised_qtitles, get_questions, Tokenizer

#python packages
import pdb
import math
import json
from pyquery import PyQuery
from pymongo import MongoClient
from pycorenlp import StanfordCoreNLP

DATA_FILE = "data/testng.csv" 


def serialize_task(task, parser):
    best_answer = None
    best_score = -1

        
    for answer in task["answers"]:
        if answer["score"] > best_score:
            best_score = answer["score"]
            best_answer = answer

    return {
        "id": parser.id,
        "title": task["title"],
        "answers": task["answers"],
        "best_answer": best_answer,
        "tags": parser.tags_str,
    }



def connect():
    #connect to mogno server and get a db object
    client = MongoClient('localhost', 27017)
    db = client.librarytasks

    #get the collection object for venue names and info
    return db.tasks


def get_core_obj():
    nlp = StanfordCoreNLP('http://localhost:9000')
    return nlp


def get_sentence_str(sentence):
    res = ""
    for token in sentence['tokens']:
        res += token['word'] + " "

    return res

def run():
    # make connections to required servies
    nlp = get_core_obj()
    tasks_db = connect()

    # questions = get_qtitles()[:1000]
    all_res = []
    questions = get_questions()[3535:]

    questions = None

    with open("all_top.json", "r") as f:
        questions = json.load(f)


    for link, question in questions.items():
        parser = SentenceParser(link, question, nlp)

        if int(question["score"]) < 1:
            continue

        if parser.is_task():
            task = parser.get_task()
            best_answer = None

            try:
                best_answer = parser.get_best_answer()
            except:
                print("Error fetching answers for id: {}".format(link))
                continue
            
            answers = []

            if len(parser.answers) < 1:
                continue

            if not best_answer:
                continue

            for answer in parser.answers:
                answers.append({
                        "body": answer.body, 
                        "code_snippets": Tokenizer.tokenize_code(answer.body),
                        "score": answer.score
                    })


            # db_ready_object = serialize_task({
            #         "title": task,
            #     }, parser)

            db_ready_object = {
                "link": link,
                "answers": answers,
                "best_answer": {
                    "body": best_answer.body,
                    "code_snippets": Tokenizer.tokenize_code(best_answer.body),
                    "score": best_answer.score
                },
                "type": question["type"],
                "title": task,
                "body": question["body"],
                "tags": question["tags"],
                "score": int(question["score"]),
                "library": question["library"],
            }

            if question.get("type", None) == "top":
                db_ready_object["sims"] = question["sims"]

            print("Inserting task into db: {}".format(task))
            tasks_db.insert_one(db_ready_object)


def find_similars():
    tasks_db = connect()

    all_items = list(tasks_db.find())

    for i in range(len(all_items)):
        sims = []

        one = all_items[i]["title"]

        for j in range(len(all_items)):
            if not i == j:
                two = all_items[j]["title"]
                try:

                    if shingling(one, two) > 0.6:
                        sims.append(all_items[j]["id"])
                except:
                    continue


        print("List of sims for {}: {}".format(i, sims))
        tasks_db.update({"id": i}, {
            "$set": {
                "sims": sims,
            }
        })
        # pdb.set_trace()


def tokenize_HTML(html):
    sentences = ""
    pq = PyQuery(html)
    
    codes = pq.children("p code").items()


    for code in codes:
        html = html.replace(code.text(), "CODE_ELEMENT_NN")


    html = html.replace("<code>", "")
    html = html.replace("</code>", "")


    new_pq = PyQuery(html)

    p_s = new_pq.children("p").items()
    for p in p_s:

        sentences = sentences + p.text() + " "

    return sentences


def get_sentences(annotated):
    par = []

    for sentence in annotated['sentences']:
        res = ""
        for word in sentence['tokens']:
            res += word['word'] + " "

        par.append(res)

    return par
            
def get_inline_snippets(html):
    pq = PyQuery(html)
    codes = ["<code>" + item.text() + "</code>" for item in pq.children("p code").items()]
    return codes


def create_dataset():
    tasks_db = connect()
    corenlp = get_core_obj()

    all_items = list(tasks_db.find())

    csv = open("../data.csv", "w") 

    columnTitleRow = "Sentence\n"
    csv.write(columnTitleRow)


    for task in all_items:
        for answer in task['answers']:
            answer_text = tokenize_HTML(answer['body'])
            #answer_text = "I would like to say hello to everyone here today. The cat is 100 years old. It's called Benyamin."
            annotated_text = corenlp.annotate(answer_text, properties = {
                #list of all annotators: tokenize,ssplit,pos,depparse,parse
                'annotators': 'depparse,pos,coref',
                'outputFormat': 'json'
            })

            sentences = get_sentences(annotated_text)

            # for key, value in annotated_text['corefs'].items():
            #     for item in value:
            #         print("\tword:{}, pos: {}".format(value['text'], value['position']))
            #         print("\t{}: {}, {}".format(len(value), value[0]['text'], value[1]['text']))

            #     print("Word: {}, Position: {}".format(item['text'], item['position'].__str__()))


            snippets = get_inline_snippets(answer['body'])

            i = 0
            numoccur = 0

            for j in range(len(sentences)):

                while "CODE_ELEMENT_NN" in sentences[j] and i < len(snippets):
                    temp_str = sentences[j].replace("CODE_ELEMENT_NN", snippets[i], 1)
                    sentences[j] = temp_str
                    i += 1

            # for item in sentences: 
            #     print("Sentence: " + item)

          
            for item in sentences:
                if "CODE_ELEMENT_NN" in item:
                    continue
                    
                sentence = item.strip()\
                .replace("\n", " ")\
                .replace("<br>", "")\
                .replace(",", "")\
                .replace('"','')\
                .replace("'", "")\
                .replace(":", "")\
                .replace("=", "")\
                .replace(".", "")\
                .strip()

                if sentence and not sentence == "":
                    row_str = sentence + "\n"
                    # print("------------------------------------------------------------------------------")
                    # print(sentence)
                    # print(row_str)
                    # print("------------------------------------------------------------------------------")
                    # pdb.set_trace()
                    csv.write(row_str)




            

def write_csv():
    csv = open("../data.csv", "w") 

    columnTitleRow = "Sentence, My Label, Your Label\n"
    csv.write(columnTitleRow)

    dataset = []
    with open(DATA_FILE) as f:
        dataset = json.load(f)['data']

    dataset = dataset[:800]



    for item in dataset:
        sentence = item["sentence"].strip().replace("\n", " ").replace("<br>", "").replace(",", "").replace('"','').replace("'", "").replace(":", "").replace("=", "").replace(".", "").strip()
        if sentence and not sentence == "" and not len(item['words']) < 4:
            row_str = sentence + "," + item['label'].__str__() + ",0\n"
            print("------------------------------------------------------------------------------")
            print(sentence)
            print(row_str)
            print("------------------------------------------------------------------------------")
            pdb.set_trace()
            csv.write(row_str)


def build_summary():
    db = connect()
    res = db.find()

    testng_items = []

    for item in res: 
        if item.get("tags", None):
            if "testng" in item["tags"]:
                print(item["tags"])
                testng_items.append(item)

    good_items = []

    for item in testng_items:
        if item.get("best_answer", None):
            good_items.append({
                    "task": item["title"],
                    "score": item["best_answer"]["score"]
                })

    sort = sorted(good_items, key=lambda x: x["score"], reverse=True)
    # pdb.set_trace()


    for i in range(20):
        print("* " + sort[i].__str__()) 

    # for i in range(10):
    #     print("* " + sort[math.floor(len(sort) / 2) + i]["task"])
    #     print("* " + sort[math.floor(len(sort) / 2) - i]["task"])


def conditional_corenlp():
    nlp = get_core_obj()
    sentence = 'I suggest this because if you want to do "advanced" things, such as installing ImageMagick/RMagick, or memcached, or a number of other plugins which require native C libraries, it becomes very painful very quickly if youre on windows.'
    
    annotated_text = nlp.annotate(sentence, properties = {
        #list of all annotators: tokenize,ssplit,pos,depparse,parse
        'annotators': 'depparse,pos,',
        'outputFormat': 'json'
    })
    print("GOT OUTPUT")
    pdb.set_trace()
    out = annotated_text['sentences'][0]



if __name__ == "__main__":
    # run()
    #find_similars()
    #write_csv()
    # create_dataset()
    # build_summary()
    conditional_corenlp()