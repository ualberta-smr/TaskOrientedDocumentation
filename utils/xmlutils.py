def serialize_task(task, ID):
    best_answer = None
    best_score = -1

        
    for answer in task["answers"]:
        if answer["score"] > best_score:
            best_score = answer["score"]
            best_answer = answer

    return {
        "id": ID,
        "title": task["title"],
        "answers": task["answers"],
        "best_answer": best_answer,
    }


def serialize_answer(answer):
    pass