from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import json
from secrets import email
from secrets import password
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pandas
import pyperclip
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from difflib import SequenceMatcher



browser = webdriver.Chrome(ChromeDriverManager().install())
options = webdriver.ChromeOptions();
options.add_argument('headless');
options.add_argument('window-size=1200x600');
browser.get('https://console.dialogflow.com/api-client/authorize_url_google/nopopup')

def __init__():
    # email
    emailElem = browser.find_element_by_xpath("//*[@id='identifierId']")
    # email = input("Input email ")
    emailElem.send_keys(email)
    submitElem = browser.find_element_by_xpath("//*[@id='identifierNext']")
    submitElem.click()

    time.sleep(2)

    # password
    passwordElem = browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
    # password = input("Input password ")
    passwordElem.send_keys(password)
    submitElem = browser.find_element_by_xpath("//*[@id='passwordNext']")
    submitElem.click()

    time.sleep(10)

if __name__ == "__main__":
    __init__()

    colnames = ['number', 'question', 'answer']
    data = pandas.read_csv('../data/msf.csv', names=colnames)

    colnames2 = ['number', 'question']
    data2 = pandas.read_csv('../data/_5_rndm_qns_test.csv', names=colnames2)
    print(data2)

    totalcount = len(data2)
    print(totalcount)
    counter = 0
    match = 0

    while(counter < totalcount):
        try:
            querybar = browser.find_element_by_xpath("//*[@id='test-client-query-input']")
            queryinput = str(data2.question[counter])
            queryinput = queryinput.replace("\r\n", "")
            pyperclip.copy(queryinput)
            querybar.send_keys(Keys.CONTROL + "v")
            querybar.send_keys(Keys.ENTER)
            print('user question: ' + queryinput)

            time.sleep(2)

            answer = browser.find_element_by_xpath("//*[@id='test-console']/div[2]/div[4]/div[4]/console-response-content/div[2]/div[2]/div/div/div/div/span/span").text
            questionnumber = data2.number[counter]
            perfectquestion = str(data.question[questionnumber])
            perfectquestion = perfectquestion.replace("\r\n", "")
            print('standard question: ' + perfectquestion)
            perfectanswer = str(data.answer[questionnumber])
            perfectanswer = perfectanswer.replace("\r\n", "")

            print('returned answer: ' + answer)
            print('standard answer: ' + perfectanswer)

            if(SequenceMatcher(None, answer, perfectanswer).ratio() > 0.8):
                match = match + 1
                print('Score: ' + str(SequenceMatcher(None, answer, perfectanswer).ratio()))
                print(str(match) + ' matches')

            #remove
            querybar.send_keys(Keys.CONTROL + "a")
            querybar.send_keys(Keys.DELETE)
            querybar.send_keys(Keys.ENTER)

            counter = counter + 1
            print('counter: ' + str(counter))
            print('\r\n')

        except UnexpectedAlertPresentException:
            pass
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass

    final = (match / totalcount) * 100
    print(final)



