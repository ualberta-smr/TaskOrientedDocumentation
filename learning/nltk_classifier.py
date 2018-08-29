#!/usr/bin/env python3

import pdb
import csv
import pickle
import string

from random import shuffle

from pycorenlp import StanfordCoreNLP

from sentiments import timeit, identity

from nltk import pos_tag
from nltk import sent_tokenize
from nltk import WordNetLemmatizer
from nltk import wordpunct_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split as tts
from sklearn.naive_bayes import MultinomialNB, BernoulliNB


TEST_DATA = [
    "As you should know Java types are divided <code>boolean</code>o primitive types <code>int</code> <code>null</code> etc and reference types",
    "Reference types in Java allow you to use the special value <code>NullPointerException</code> which is the Java way of saying `` no object",
    "A NullPo<code>null</code>erException is thrown at runtime whenever your program attempts to use a <code>length()</code> as if it was a real reference",
    "For example if you write this the statement labelled `` HERE is going to attempt to run the <code>null</code> method on a <code>NullPointerException</code> reference and this will throw a NullPo<code>null</code>erException",
    "There are many ways that you could use a <code>NullPointerException</code> value that will result in a NullPo<code>null</code>erException",
    "If fact the only things that you can do with a <code>javac</code> without causing an NPE are Sup<code>foo</code>e that I compile and run the program above First observation the compilation succeeds !",
    "The problem in the program is NOT a compilation error",
    "Not recommended but this is also a way",
    "This snippet was found in \ sdk \ samples \ android-19 \ connectivity \ NetworkConnect \ NetworkConnectSample \ src \ main \ java \ com \ example \ android \ networkconnect \ MainActivityjava which is licensed under Apache License Version 20 and written by Google",
    "I have written a class that does just that so I figured I d share it with everyone",
    "Sometimes you do nt want to add Apache Commons just for one thing and want something dumber than Scanner that does nt examine the content",
    "Usage is as follows Here is the code for ReaderSink",
    "Here is the complete method for converting <code>InputStream</code> into <code>String</code> without using any third party library",
    "Use <code>StringBuilder</code>Builder for single threaded environment otherwise use <code>StringBuffer</code>Buffer",
    "I had log4j available so I was able to use the orgapachelog4jlf5utilStreamUtilsgetBytes to get the bytes which I was able to convert into a string using the String ctor",
    "This one is nice because What the for ?",
    "I d use some Java 8 tricks",
    "Essentially the same as some other answers except more succinct",
    "This is an answer adapted from <code>orgapachecommonsioIOUtils</code> source code for those who want to have the apache implementation but do not want the whole library",
    "The following does nt address the original question but rather some of the responses",
    "Several responses suggest loops of the form or The first form pollutes the namespace of the enclosing scope by declaring a variable `` read in the enclosing scope that will not be used for anything outside the for loop",
    "The second form duplicates the readline call",
    "Here is a much cleaner way of writing this sort of loop in Java",
    "It turns out that the first clause in a for-loop does nt require an actual initializer value",
    "This keeps the scope of the variable `` line to within the body of the for loop",
    "Much more elegant !",
    "I have nt seen anybody using this form anywhere I randomly discovered it one day years ago but I use it all the time",
    "Kotlin users simply do whereas is Kotlin standard library s built-in extension method",
    "Pure Java solution using Stream s works since Java 8",
    "As mentioned by Christoffer Hammarström below other answer it is safer to explicitly specify the Charset",
    "If you ca nt use Commons IO FileUtils/IOUtils/CopyUtils here s an example using a BufferedReader to read the file line by line or if you want raw speed I d propose a variation on what Paul de Vrieze suggested which avoids using a StringWriter which uses a StringBuffer internally",
    "If you are using Google-Collections/Guava you could do the following Note that the second parameter ie CharsetsUTF _ 8 for the <code>InputStreamReader</code> is nt necessary but it is generally a good idea to specify the encoding if you know it which you should !",
    "First you have to know the encoding of string that you want to convert",
    "Because the <code>javaioInputStream</code> operates an underlying array of bytes however a string is composed by a array of character that needs an encoding e g UTF-8 the JDK will take the default encoding that is taken from If <code>inputStream</code> s byte array is very big you could do it in loop",
    "Here s a way using only standard Java library note that the stream is not closed YMMV",
    "I learned this trick from `` Stupid <code>Scanner</code> tricks article",
    "Hat tip goes also to Jacob who once pointed me to the said article",
    "EDITED Thanks to a suggestion from Patrick made the function more robust when handling an empty input stream",
    "One more edit nixed try/catch Patrick s way is more laconic",
    "I ran The error is misleading <code>Unsupported majorminor version 510</code>",
    "This gives the impression that version 51 Java 7 is not supported",
    "And we should use Java 6",
    "The error should have been",
    "I got the same problem with a project written in 17 and tried to execute in 16",
    "My solution in Eclipse That worked for me",
    "You have used a higher version of the JDK to compile and trying to run from a lower version of JDK / JRE",
    "To check this see the version information They will be different and javac will have a higher version number",
    "To get around this run using java from the JDK version or if you have a newer JRE/JDK that will work as well",
    "This is related to Java Access Modifiers",
    "From Java Access Modifiers From Controlling Access to Members of a Class tutorials",
    "Often times I ve realized that remembering the basic concepts of any language can made possible by creating real-world analogies",
    "Here is my analogy for understanding access modifiers in Java Let s assume that you re a student at a university and you have a friend who s coming to visit you over the weekend",
    "Suppose there exists a big statue of the university s founder in the middle of the campus",
    "Hope this helps !",
    "When you are thinking of access modifiers just think of it in this way applies to both variables and methods <code>public</code> -- > accessible from every where <code>private</code> -- > accessible only within the same class where it is declared Now the confusion arises when it comes to <code>default</code> and <code>protected</code> <code>default</code> -- > No access modifier keyword is present",
    "This means it is available strictly within the package of the class",
    "Nowhere outside that package it can be accessed",
    "<code>protected</code> -- > Slightly less stricter than <code>default</code> and apart from the same package classes it can be accessed by sub classes outside the package it is declared",
    "Or with generics You can of course replace string with any type of variable such as Integer also",
    "or with generics",
    "First read this then read this and this",
    "9 times out of 10 you ll use one of those two implementations",
    "In fact just read Sun s Guide to the Collections framework",
    "Additionally if you want to create a list that has things in it",
    "List is just an interface just as Set",
    "Like HashSet is an implementation of a Set which has certain properties in regards to add / lookup / remove performance ArrayList is the bare implementation of a List",
    "If you have a look at the documentation for the respective interfaces you will find `` All Known Implementing Classes and you can decide which one is more suitable for your needs",
    "Chances are that it s ArrayList",
    "There are many ways to create a Set and a List",
    "HashSet and ArrayList are just two examples",
    "It is also fairly common to use generics with collections these days",
    "I suggest you have a look at what they are This is a good introduction for java s builtin collections",
    "http//javasuncom/javase/6/docs/technotes/guides/collections/overviewhtml",
    "Using Google Collections you could use the following methods in the Lists class There are overloads for varargs initialization and initialising from an Iterable <T>",
    "The advantage of these methods is that you do nt need to specify the generic parameter explicitly as you would with the constructor - the compiler will infer it from the type of the variable",
    "Since Java 7 you have type inference for generic instance creation so there is no need to duplicate generic parameters on the right hand side of the assignment A fixed-size list can be defined as For immutable lists you can use the Guava library",
    "You need to import <code>List</code> and Array<code>ArrayList</code>",
    "Let me summarize and add something JDK Guava Immutable List Empty immutable List List of Characters List of Integers",
    "As an option you can use double brace initialization",
    "Its better you use generics as suggested below Incase you use LinkedList",
    "More options to do the same thing with Java 8 not better not worse just different and if you want to do some extra work with the lists Streams will provide you more alternatives filter map reduce etc",
    "Variables and methods can be declared without any modifiers that is called Default examples Private Access Modifier - private Methods Variables and Constructors that are declared private can only be accessed within the declared class itselfPrivate access modifier is the most restrictive access level",
    "Class and interfaces can not be private",
    "Variables that are declared private can be accessed outside the class if public getter methods are present in the class",
    "Using the private modifier is the main way that an object encapsulates itself and hide data from the outside world",
    "examples Public Access Modifier - public A class method constructor interface etc declared public can be accessed from any other class",
    "Therefore fields methods blocks declared inside a public class can be accessed from any class belonging to the Java Universe",
    "However if the public class we are trying to access is in a different package then the public class still need to be imported",
    "Because of class inheritance all public methods and variables of a class are inherited by its subclasses",
    "example Protected Access Modifier - protected Variables methods and constructors which are declared protected in a superclass can be accessed only by the subclasses in other package or any class within the package of the protected members class",
    "The protected access modifier can not be applied to class and interfaces",
    "Methods fields can be declared protected however methods and fields in a interface can not be declared protected",
    "Protected access gives the subclass a chance to use the helper method or variable while preventing a nonrelated class from trying to use it",
    "I just want to address a detail that is extremely commonly got wrong including by most of the answers on this page",
    "Default access when no access modifier is present is not always the same as package-private",
    "I tried all the methods in stackoverflow and also in youtube",
    "non of them worked for me untill i found this easy method",
    "I installed 64bit java form Cnet download and the problem was automatically fixed",
    "I mentioned the source because it is too easy to google and go to first Cnet lint rather than oficial site if you are a new bee",
    "ps if you have Android ADT bundle and tried to open eclipse from it and got the same error you can fix that problem too with this method",
    "I m not sure why but I had the jre installed into my c \ windows directory and javaexe and javawexe inside my windows \ system32 directory",
    "Obviously these directories were getting priority even AFTER adding the - vm flag to my eclipseini file",
    "Delete them from here fixed the issue for me",
    "In my case I tried to launch java from the command prompt and got this error It meant `` java was looked for in the PATH starting at this wrong directory",
    "Deleting the folder C \ Windows \ jre \ solved the issue",
    "The easiest solution is to include a specific JRE in eclipseini wikieclipseorg/Eclipseini With this you can start almost any Eclipse version",
    "This error means that the architecture of Eclipse does not match the architecture of the Java runtime ie if one is 32-bit the other must be the same and not 64-bit",
    "The most reliable fix is to specify the JVM location in eclipseini Important These two lines must come before - vmargs",
    "Do not use quotes ; spaces are allowed",
    "I want to previde another solution for this error especially for who want to use 32-bit and 64-bit Eclipse in one system",
    "Eclipse will startup using the JRE/JDK in <code>jre</code> sub-directory if it exists",
    "STS or other eclipse based IDE also support this feature The solution is create directory junction using <code>mklinkexe</code> command which exist in windows vista or newer version junctionexe offer similar function for Windows 2000/XP Open the command line windows and exeute following command Of course if the Eclipse is for 64-bit Windows the architecture of <code>JDK/JRE</code> must be the same",
    "Assume The command for creating the <code>jre</code> folder will be BTW delete directory junction will NOT delete any file",
    "If you create a wrong link you can delete it using file explorer or <code>rmdir</code> command",
    "The official tutorial may be of some use to you",
    "if you have not restarted your computer after installing jdk just restart your computer",
    "if you want to make a portable java and set <code>java_home</code> before using java just make a batch file i explained below",
    "if you want to run this batch file when your computer start just put your batch file shortcut in startup folder",
    "In windows 7 startup folder is `` C \ Users \ user \ AppData \ Roaming \ Microsoft \ Windows \ Start Menu \ Programs \ Startup make a batch file like this note <code>path</code> and <code>set amirgood_boy</code> are variables",
    "you can make any variable as you wish",
    "We need to make a distinction between the two environment variables that are discussed here interchangeably"
]

DATA_FILE = "data_training.csv" 
PATH = "res.model"

class NLTKPreprocessor(BaseEstimator, TransformerMixin):

    def __init__(self, stopwords=None, punct=None,
                 lower=True, strip=True):
        self.lower      = lower
        self.strip      = strip
        self.stopwords  = stopwords or set(sw.words('english'))
        self.punct      = punct or set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, X):
        return [
            list(self.tokenize(doc)) for doc in X
        ]

    def tokenize(self, document):
        # Break the document into sentences
        for sent in sent_tokenize(document):
            # Break the sentence into part of speech tagged tokens
            for token, tag in pos_tag(wordpunct_tokenize(sent)):
                # Apply preprocessing to the token
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token
                token = token.strip('_') if self.strip else token
                token = token.strip('*') if self.strip else token

                # If stopword, ignore token and continue
                if token in self.stopwords:
                    continue

                # If punctuation, ignore token and continue
                if all(char in self.punct for char in token):
                    continue

                # Lemmatize the token and yield
                lemma = self.lemmatize(token, tag)
                yield lemma

    def lemmatize(self, token, tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

@timeit
def build_and_evaluate(X, y,
    classifier=SGDClassifier, outpath=None, verbose=True):

    @timeit
    def build(classifier, X, y=None):
        """
        Inner build function that builds a single model.
        """
        if isinstance(classifier, type):
            classifier = classifier()

        model = Pipeline([
            ('preprocessor', NLTKPreprocessor()),
            ('vectorizer', TfidfVectorizer(
                tokenizer=identity, preprocessor=None, lowercase=False
            )),
            ('classifier', classifier),
        ])

        model.fit(X, y)
        return model

    # Label encode the targets
    labels = LabelEncoder()
    y = labels.fit_transform(y)

    # Begin evaluation
    if verbose: print("Building for evaluation")
    X_train, X_test, y_train, y_test = tts(X, y, test_size=0.2)
    model, secs = build(classifier, X_train, y_train)

    if verbose:
        print("Evaluation model fit in {:0.3f} seconds".format(secs))
        print("Classification Report:\n")

    y_pred = model.predict(X_test)
    print(clsr(y_test, y_pred, target_names=labels.classes_))

    if verbose:
        print("Building complete model and saving ...")
    model, secs = build(classifier, X, y)
    model.labels_ = labels

    if verbose:
        print("Complete model fit in {:0.3f} seconds".format(secs))

    if outpath:
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)

        print("Model written out to {}".format(outpath))


    model.predict(TEST_DATA)


    return model


def get_core_obj():
    nlp = StanfordCoreNLP('http://localhost:9000')
    return nlp


def main(nlp):
    dataset = []
    with open(DATA_FILE) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            res = ""
            annotated_text = nlp.annotate(row[0], properties = {
                'annotators': 'pos',
                'outputFormat': 'json'
            })

            if len(annotated_text['sentences']) > 1:
                print("WEIRD SHIT HAPPENING")
                continue

            for item in annotated_text['sentences'][0]['tokens']:
                res += item['word'] + " "

            dataset.append({
                "sentence": res + ".",
                "label": row[1]
            })

    pos_all = [{'sentence': item['sentence'], 'label': 'pos'} for item in dataset if item['label'] == "1"]
    neg_all = [{'sentence': item['sentence'], 'label': 'neg'} for item in dataset if item['label'] == "0"]

    learn_ready = pos_all + neg_all


    shuffle(learn_ready)
    X = [item["sentence"] for item in learn_ready]
    y = [item["label"] for item in learn_ready]

    # model = build_and_evaluate(X,y, classifier=RandomForestClassifier, outpath=PATH)
    # model, secs = build_and_evaluate(X,y, classifier=BernoulliNB, outpath=PATH)
    model, seconds = build_and_evaluate(X,y, outpath=PATH)

    pred = model.predict(TEST_DATA)

    # pdb.set_trace()

    for i in range(len(pred)):
        if pred[i] == 1:
            print(TEST_DATA[i])


if __name__=="__main__":
    nlp = get_core_obj()
    main(nlp)