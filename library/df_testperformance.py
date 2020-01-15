import argparse
import json
import xml.etree.ElementTree as ET
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--test_questions", type=str, help="Path to newline separated questions stored in txt file")
    arg_parser.add_argument("--output", type=str, help="Path to json output file")
    args = arg_parser.parse_args()

    with open(args.test_questions, 'r', encoding='utf-8') as f:
        questions = [line.strip() for line in f]

    url = "https://va.ecitizen.gov.sg/flexAnsWS/ifaqservice.asmx/AskWSLanguage"
    partial_payload = {"ProjectId": 7536554, "RecordQuestion": "yes", "SessionId": 0, "TextLanguage": "en"}
    results = defaultdict(list)
    for question in questions:
        # send API request to get answers
        payload = partial_payload.copy()
        payload.update({"Question": question})
        xml_string = requests.post(url, data=payload).text
        # parse xml string
        root = ET.fromstring(xml_string)
        count = int(root.find("Count").text)
        if count == 0:
            results[question] = []
            continue

        # parse html string
        raw_answers = [e.find("{urn:agathos-com:imfinity:flexanswer:data:v1}Text").text for e in
                       root.find("Responses").findall("Response")]

        for raw_answer in raw_answers:
            answer = BeautifulSoup(raw_answer, features='html5lib').text
            print(answer)
            results[question].append(answer)

    assert len(results) == len(questions)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f)
