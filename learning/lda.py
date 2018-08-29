#!/usr/bin/env python3


#self defined packages
#from utils.serializer import serialize_task
import pdb
import csv
import gensim
from gensim import corpora, models
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer


def get_qtitles():
    INPUT_FILES = ["data/junit.csv", "data/testng.csv"]
    titles = []
    for input_file in INPUT_FILES:
        with open(input_file, mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                titles.append(row[1].lower())


    titles.pop(0)
    return titles



def prepare_dataset():
    questions = get_qtitles()
    print(len(questions))
    dataset = []

    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = get_stop_words('en')

    all_stop = set()

    for item in en_stop:
        all_stop.add(item)


    all_stop.add("testng")
    all_stop.add("junit")

    p_stemmer = PorterStemmer()

    for data in questions:
        tokens = tokenizer.tokenize(data.lower())
        stopped_tokens = [i for i in tokens if not i in all_stop]
        texts = [p_stemmer.stem(i) for i in stopped_tokens]

        dataset.append(texts)


    return dataset


def run():
    dataset = prepare_dataset()

    dictionary = corpora.Dictionary(dataset)
    corpus = [dictionary.doc2bow(text) for text in dataset]

    for num_topics in range(2, 10):
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=20)
        print("Num Topics: {}".format(num_topics))
        print(ldamodel.print_topics(num_topics=num_topics, num_words=10))
    

if __name__ == "__main__":
    run()