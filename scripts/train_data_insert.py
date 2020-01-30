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

    colnames = ['number', 'question']
    data = pandas.read_csv('../data/_5_rndm_qns_train.csv', names=colnames)

    colnames2 = ['number', 'question', 'answer']
    data2 = pandas.read_csv('../data/msf.csv', names=colnames2)
    print(data)

    number = data.number.tolist()
    totalcount = len(number)
    counter = 929
    while(counter < totalcount):
        try:
            #search intent
            searchIntentBar = browser.find_element_by_xpath("//*[@id='input-search-intents']")
            searchIntentBar.send_keys(Keys.CONTROL + "a")
            searchIntentBar.send_keys(Keys.DELETE)
            question_number = data.number[counter]
            print(question_number)
            question = data2.question[question_number]
            print(question)
            intentname = question.replace(" ", "_")
            intentname = intentname.replace("\r\n", "")
            intentname = str(int(question_number)) + '-' + intentname[0:95]
            pyperclip.copy(intentname)
            searchIntentBar.send_keys(Keys.CONTROL + "v")
            searchIntentBar.send_keys(Keys.ENTER)

            #get first intent
            firstintent = browser.find_element_by_xpath("//*[@id='main']/div/div[3]/div/div/div[2]/ul/li[1]/intents-list-item/div/div/span/span[2]/span")
            firstintent.click()

            time.sleep(5)

            #add training phrase
            addquestion = browser.find_element_by_xpath("//*[@id='intent-user-says-editor']/intent-user-says-editor/div[2]/div[1]/user-says-editor/div/div/div[1]/div")
            question2 = str(data.question[counter])
            question2 = question2.replace("\r\n", "")
            pyperclip.copy(question2)
            addquestion.send_keys(Keys.CONTROL + "v")
            addquestion.send_keys(Keys.ENTER)
            # time.sleep(2)

            #save
            save = browser.find_element_by_xpath("//*[@id='multi-button']")
            save.click()
            print("save")

            time.sleep(2)

            #next
            exit = browser.find_element_by_xpath("//*[@id='link-list-intents']")
            exit.click()
            print("exit")
            time.sleep(2)

            counter = counter + 1
            print(counter)

        except UnexpectedAlertPresentException:
            alert = browser.switch_to.alert
            alert.dismiss()

            time.sleep(2)
            # save
            save = browser.find_element_by_xpath("//*[@id='multi-button']")
            save.click()
            print("save")

            time.sleep(2)

            exit = browser.find_element_by_xpath("//*[@id='link-list-intents']")
            exit.click()
            print("try to exit again")
            time.sleep(2)

        except NoSuchElementException:
            pass

        except ElementNotInteractableException:
            pass





