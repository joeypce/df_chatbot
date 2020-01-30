from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import json
from secrets import email
from secrets import password
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

browser = webdriver.Chrome(ChromeDriverManager().install())
options = webdriver.ChromeOptions();
options.add_argument('headless');
options.add_argument('window-size=1200x600');
browser.get('https://console.dialogflow.com/api-client/authorize_url_google/nopopup')
try:

    # email
    emailElem = browser.find_element_by_xpath("//*[@id='identifierId']")
    # email = input("Input email ")
    emailElem.send_keys(email)
    submitElem = browser.find_element_by_xpath("//*[@id='identifierNext']")
    submitElem.click()

    time.sleep(1)

    # password
    passwordElem = browser.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
    # password = input("Input password ")
    passwordElem.send_keys(password)
    submitElem = browser.find_element_by_xpath("//*[@id='passwordNext']")
    submitElem.click()

    time.sleep(10)

    # search intent
    searchIntentBar = browser.find_element_by_xpath("//*[@id='input-search-intents']")
    searchIntentBar.send_keys("3-Is_there_a_validity_period_to_be_a_Baby_Bonus_Approved_Institution?")
    searchIntentBar.send_keys(Keys.ENTER)

    # get first intent
    firstintent = browser.find_element_by_xpath(
        "//*[@id='main']/div/div[3]/div/div/div[2]/ul/li[1]/intents-list-item/div/div/span/span[2]/span")
    firstintent.click()


    # # select intent
    # intentElem = browser.find_element_by_xpath("//*[contains(text(), 'when-was-baby-bonus-implemented')]")
    # intentElem.click()

    time.sleep(5)

    # get question
    insertQuestionElem = browser.find_element_by_xpath(
        "//*[@id='intent-user-says-editor']/intent-user-says-editor/div[2]/div[2]/user-says-editor/div/div[1]/div[1]/div").text
    print(insertQuestionElem)

    url = 'http://155.69.146.209:80/question_generation-service'
    data = json.dumps({"questions": [insertQuestionElem],
                       "lemmatize": False,
                       "apply_synonym": False
                       })

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data, headers=headers)

    data = json.loads(r.text)
    print(data)
    print(type(data))

    # insert question permutation into training phrases
    # format string
    r = r.text
    r = r.replace('",', '\n')
    r = r.replace('"', '')
    r = r.replace('[', '')
    r = r.replace(']', '')
    r = r.replace('}', '')
    r = r.replace('{', '')
    r = r.replace(':', '\n')
    print(r)

    formattedresult = r.split('\n')
    formattedresult = formattedresult[-30:]
    print(len(formattedresult))

    inputElem = browser.find_element_by_xpath(
        "//*[@id='intent-user-says-editor']/intent-user-says-editor/div[2]/div[1]/user-says-editor/div/div/div[1]/div")

    for i in range(len(formattedresult)):
        if(insertQuestionElem != formattedresult[i]):
            inputElem.send_keys(formattedresult[i])
            inputElem.send_keys(Keys.ENTER)

except:
    print('Error')
