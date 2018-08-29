#list of stop all_words", 
STOP_all_words = {
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "+",
    "-",
    "/",
    "=",
    "'ve",
    "'s",
    "'ll",
    "'d",
    "if",
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
    "ours   ourselves", 
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
}


PUNCTUATION = {"!", ".", ",", "?", "(", ")", "[", "]", "{", "}", ":", ";", "-"}


def tokenize(task):
    temp = task
    for item in PUNCTUATION:
        temp = temp.replace(item, "")


    tokens = temp.split(" ")
    tokens_list = []
    for token in tokens:
        token = token.replace(" ", "")
        if not token == "":
            tokens_list.append(token)

    if len(tokens_list) > 0: 
        return tokens_list




def jaccard(one, two): 
    one_tokens = tokenize(one.lower())
    two_tokens = tokenize(two.lower())

    all_words = set()
    intersect = set()

    for token in one_tokens: 
        if not token in all_words:
            all_words.add(token)

    for token in two_tokens: 
        if not token in all_words:
            all_words.add(token)

    for token in all_words:
        if token in one_tokens and token in two_tokens:
            intersect.add(token)


    return len(intersect) / len(all_words)


def cosine(one, two):
    one_tokens = tokenize(one.lower())
    two_tokens = tokenize(two.lower())

    all_words = []

    for token in one_tokens: 
        if not token in all_words:
            all_words.add(token)

    for token in two_tokens: 
        if not token in all_words:
            all_words.add(token)

    one_vector = [False] * len(all_words)
    two_vector = [False] * len(all_words)



def shinglize(tokens):
    shingles = []
    for i in range(len(tokens) - 1):
        string = tokens[i] + " " + tokens[i + 1]
        shingles.append(string)

    return shingles



def shingling(one, two):
    one_tokens = tokenize(one.lower())
    two_tokens = tokenize(two.lower())

    one_shingles = shinglize(one_tokens)
    two_shingles = shinglize(two_tokens)


    all_words = set()
    intersect = set()

    for token in one_shingles:
        if not token in all_words:
            all_words.add(token)

    for token in two_shingles: 
        if not token in all_words:
            all_words.add(token)

    for token in all_words:
        if token in one_shingles and token in two_shingles:
            intersect.add(token)


    return len(intersect) / len(all_words)







def get_similar_tasks(tasks):
    for i in range(0, len(tasks) - 1):
        for j in range(i+1, len(tasks)):
            sim = shingling(tasks[i], tasks[j]) 
            if sim > 0.6:
                print(tasks[i] + " <--------> " + tasks[j])