import argparse
import json
import xml.etree.ElementTree as ET
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

# if __name__ == '__main__':
def calljamie(question):
    url = "https://va.ecitizen.gov.sg/flexAnsWS/ifaqservice.asmx/AskWSLanguage"
    partial_payload = {"ProjectId": 7536554, "RecordQuestion": "yes", "SessionId": 0, "TextLanguage": "en"}
    payload = partial_payload.copy()
    payload.update({"Question": question})
    xml_string = requests.post(url, data=payload).text
    root = ET.fromstring(xml_string)
    count = int(root.find("Count").text)
    raw_answers = [e.find("{urn:agathos-com:imfinity:flexanswer:data:v1}Text").text for e in
                   root.find("Responses").findall("Response")]

    for raw_answer in raw_answers:
        # answer = BeautifulSoup(raw_answer, features='html5lib').text
        print(raw_answer)
        return raw_answer
        # results[question].append(answer)

    # assert len(results) == len(questions)
    # with open(args.output, 'w', encoding='utf-8') as f:
    #     json.dump(results, f)