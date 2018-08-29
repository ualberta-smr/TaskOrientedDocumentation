#!/usr/bin/env python3


#self defined packages
#from utils.serializer import serialize_task
from taskidentification.taskid import SentenceParser
from taskidentification.similarity import get_similar_tasks, shingling
from utils.nlputils import VERB_IDENTIFIERS, NOUN_IDENTIFIERS
from taskidentification.similarity import STOP_all_words, PUNCTUATION
from utils.fileutils import get_qtitles, supervised_qtitles, get_questions, Tokenizer

#python packages
import os
import csv
import pdb
import math
import json
from pyquery import PyQuery
from pymongo import MongoClient
from pycorenlp import StanfordCoreNLP

FINAL_SET = {}

DATA_PATH = "csvs/"


index = {
    'id': 0,
    'title': 1,
    'body': 2,
    'tags': 3,
    'score': 4,
    'sims': 5,
    'accepted_id': 6,
}


def find_similars(item, all_items):

    sims = []

    one = item[index["title"]]

    for i in range(len(all_items)):
        if not item == all_items[i]:
            two = all_items[i][index["title"]]
            try:
                if shingling(one, two) > 0.6:
                    sims.append(two[index["id"]])
            except:
                continue
    # print()

    return sims

def connect():
    #connect to mogno server and get a db object
    client = MongoClient('localhost', 27017)
    db = client.librarytasks

    #get the collection object for venue names and info
    return db.tasks


def create_dataset():
    for filename in os.listdir(DATA_PATH):
        all_sims = set()

        if filename.endswith(".csv"):
            lib_name = filename.split(".")[0]
            print("Handling file {}.".format(filename))

            with open(DATA_PATH + filename, "r") as file:

                reader = csv.reader(file)
                skip_first = False

                lib_questions = []
                for row in reader:
                    if not skip_first:
                        skip_first = True
                        continue


                    # new line in file
                    lib_questions.append(row)

                print("Found {} items in the file. Sorting items.".format(len(lib_questions)))

                lib_questions = sorted(lib_questions, key=lambda x: x[index["score"]], reverse=True)
                lib_questions_top = lib_questions[:math.floor(len(lib_questions)/10)]
                print("Searching {} items for similar threads.".format(len(lib_questions_top)))

                for item in lib_questions_top:
                    sims = find_similars(item, lib_questions)
                    item.append(sims)
                    for sim in sims:
                        all_sims.add(sim)

                for item in lib_questions_top:
                    if not FINAL_SET.get(item[index["id"]], None):
                        FINAL_SET[item[index["id"]]] = {
                            'type': 'top',
                            'title': item[index["title"]],
                            'body': item[index["body"]],
                            'tags': item[index["tags"]],
                            'score': item[index["score"]],
                            'sims': item[index["sims"]],
                            'library': lib_name,
                            'accepted_id': item[index['accepted_id']]
                        }

                for item in lib_questions:
                    if item[index["id"]] in all_sims:
                        if not FINAL_SET.get(item[index["id"]], None):
                            FINAL_SET[item[index["id"]]] = {
                            'type': 'sim',
                            'title': item[index["title"]],
                            'body': item[index["body"]],
                            'tags': item[index["tags"]],
                            'score': item[index["score"]],
                            'library': lib_name,
                            'accepted_id': item[index['accepted_id']]
                        }


                print("Done. {} items in FINAL_SET.".format(len(FINAL_SET)))
                file.close()

    with open("all_top.json", "w") as file:
        file.write(json.dumps(FINAL_SET))

    pdb.set_trace()

    db = connect()

    for link, obj in FINAL_SET.items():
        if obj.get("type", None) == "top":
            db.insert_one({
                "link": link,
                "type": obj["type"],
                "title": obj["title"],
                "body": obj["body"],
                "tags": obj["tags"],
                "score": obj["score"],
                "library": obj["library"],
                "sims": obj["sims"],
            })
        else:
            db.insert_one({
                "link": link,
                "type": obj["type"],
                "title": obj["title"],
                "body": obj["body"],
                "tags": obj["tags"],
                "score": obj["score"],
                "library": obj["library"],
            })


if __name__ == "__main__":
    create_dataset()