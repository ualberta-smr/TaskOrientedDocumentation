def serialize_task(task, ID):
    best_answer = None
    best_score = -1
    for answer in task['answers']:
        if answer["score"] > best_score:
            best_score = answer["score"]
            best_answer = answer

    return {
        "id": ID,
        "title": task['title'],
        "answers": task['answers'],
        "best_answer": best_answer,
    }


DATA_FILE = '/media/benyamin/5AF02634528B5BE8/SO Dump/Posts.xml'

def parse_xml_line(line):
    #this functions gets a line from the posts.xml file 
    #and parses the file into a dictionary object where
    #the keys are the attributes of the xml row

    res = dict()
    cur_key = None

    line_split = line.replace("<row", "").replace("/>", "").split('="')

    for index, item in enumerate(line_split):
        if index == 0: 
            cur_key = item.strip()

        else:
            item_split = item.split('"')
            res[cur_key] = item_split[0].strip()
            cur_key = item_split[1].strip()

    return res