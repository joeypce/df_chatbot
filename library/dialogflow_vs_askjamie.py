import os
import dialogflow_v2 as dialogflow
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

from library import df_detectintent
from library.call_askjamie import calljamie

from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    print(type(html))
    if(type(html) is list):
        html = ''.join(html)
    s = MLStripper()
    s.feed(html)
    return s.get_data()


filepath = 'C:\\Users\\Joey\\PycharmProjects\\FYP_UI\\data\\test_questions.txt'
answerfile = 'C:\\Users\\Joey\\PycharmProjects\\FYP_UI\\data\\test_answers.txt'
fullanswerpath = 'C:\\Users\\Joey\\PycharmProjects\\FYP_UI\\data\\answers.txt'
answer_id = open(answerfile , encoding="utf8")
aline = answer_id.readlines()

answer = open(fullanswerpath, encoding="utf8")
aline2 = answer.readlines()

with open(filepath, errors='ignore') as fp:
    line = fp.readline()
    cnt = 1
    questions = []
    answers = []
    msf_responses = []
    df_responses = []
    msf_match = []
    df_match = []

    msfmatch_count = 0
    dfmatch_count = 0

    while line:
        print("Line {}: {}".format(cnt, line.strip()))
        question = line.strip()
        answerid = int(aline[cnt-1])
        answer = aline2[answerid].strip()

        # response from dialogflow (alpha, beta, charlie)
        # output = df_detectintent.detectintent_charlie(question)
        # if ((output["intent"] == "Default Fallback Intent")):
            # call beta
        output = df_detectintent.detectintent_beta(question)
        if ((output["intent"] == "Default Fallback Intent") or len(output["response"]) == 0) and output[
            "intent"] != "ambiguous-intent":
            # call alpha
            output = df_detectintent.detectintent_alpha(question)

        output = strip_tags(output["response"])
        df_responses.append(output)

        # dialogflow performance
        output = ' '.join(output.split()[:8])
        if output in answer:
            df_match.append("true")
            dfmatch_count += 1
        else:
            df_match.append("false")

        # response from msf
        jamie = strip_tags(calljamie(question))
        jamie = jamie.replace(u'\xa0', u'')
        msf_responses.append(jamie)

        jamie = ' '.join(jamie.split()[:8])
        if jamie in answer:
            msf_match.append("true")
            msfmatch_count += 1
        else:
            msf_match.append("false")

        # ----------------------------------------------------------------
        questions.append(question)
        answers.append(answer)
        line = fp.readline()
        cnt += 1

print(questions)
print(df_responses)
print(msf_responses)
print(answers)
print(df_match)
print(msf_match)
msf_acc = (msfmatch_count/130) * 100
df_acc = (dfmatch_count/130) * 100
df = pd.DataFrame({'questions': questions
                      ,'df': df_responses,
                   'msf': msf_responses,
                   'answers': answers,
                   'msf_match?': msf_match,
                   'df_match?': df_match,
                   'acc_msf': msf_acc,
                   'acc_df': df_acc})
writer = ExcelWriter('df_vs_msf.xlsx')
df.to_excel(writer, 'Sheet2', index=False)
writer.save()

print("df matches " + str(dfmatch_count))
print("msf matches " + str(msfmatch_count))
