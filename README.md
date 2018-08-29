# Benyamin-Task-Oriented-Documentation
This repository holds the code and documents required to reproduce the outputs of task-oriented library documentation.


## Important note 

In order to initially set up the system to run this, you need to install a (rather long) list of Python packages. I've included every package installed on my computer in the requirements.txt file. You can quickly install all packages on that list by running 

pip3 install requirements.txt 

Or you can install one by one. 


Also, in order to run the code you need to have CoreNLP running on port 9000. The CoreNLP server can be downloaded from this address: https://stanfordnlp.github.io/CoreNLP/download.html

You also need a MongoDB server running on port 27017 since that's where the outputs will be saved. 



## Strucutre

The api/ folder holds code that uses the Stack Exchange API to query for threads and posts on Stack Overflow. 

The learning/ folder holds the code we used for building the classifier for insights extraction. The main part of the code in that folder is included in the sentiments.py file which trains, tests and stores the model in a file named "res.model". Note that the insight sentence extraction is done on demand. When someone in the survey, clicks on a task, we run the model against all the sentences in the related threads.

The utils/ folder holds general purpose code needed to read files and also static lists that I used throughout the project. 

The taskidentification/ folder holds the code that actulaly does the task, code and similarity extraction. Task and code extraction is included in taskid.py and similarity.py runs the similarity detection process. 

The CSVs thread is a number of CSV files, one for every library that we created documentaion for. Each of these files includes a list of the questions that have the tag of that library on Stack Overflow. These files are used by the main.py file to produce the documentation. The documentation produced will be stored in a file named all_top.json. I've included the last all_top.json produced by our methodology in this repo as well so you know what it looks like. 

build_dataset.py reads the all_top.json file and stores the data there in a MongoDB database. 
