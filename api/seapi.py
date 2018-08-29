import stackexchange


def answers_to_question(id):
    #key = 'TIIINIXcEDncTZQbPSzsiA'
    #key = 'G96PVW9Zi*voBduDLhsecA(('
    #key = 'ol7GTKMQYYd9KBwDHqq9fg(('
    so = stackexchange.Site(stackexchange.StackOverflow, "G96PVW9Zi*voBduDLhsecA((")
    so.impose_throttling = True
    so.throttle_stop = False
    so.be_inclusive()
    question = so.question(id)
    return question.answers
