from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import sys
import random
import time

def GoToEmptyGroup():
    for x in browser.find_elements_by_class_name("_1wjpf"):
        if x.get_attribute('title') == 'Testing':
            testingaction = webdriver.common.action_chains.ActionChains(browser)
            testingaction.move_to_element(x)
            testingaction.click()
            testingaction.perform()
            testingaction.click()
            testingaction.perform()
            break

run = True
jokes = []
offset = 0
offsetmax = 12
while run and offset < offsetmax:
    url = "http://www.jokes.co.il/show.php?site=default&mark=0&topic=1&offset=" + str(offset)
    print(url)
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    #type(soup)
    #print(soup)
    tables = soup.find_all('table')
    contenttable = str(tables[3])
    if contenttable.find('תומיאתמ תוחידב ואצמנ אל') == -1:
        splittedcontent = contenttable.split('<img src="http://www.jokes.co.il/images/start_joke.gif"/><br/><br/>')[1:]
        for x in range(0, len(splittedcontent)):
            towhere = splittedcontent[x].find('<br/><br/><img src="http://www.jokes.co.il/images/jbullet.gif"/>')
            removegarbage = splittedcontent[x][:towhere]
            filtertags = BeautifulSoup(removegarbage, 'lxml').get_text()
            fliphebrew = filtertags[::-1]
            splittedcontent[x] = fliphebrew.replace("</br>", "").replace('\r', '').split('\n')[::-1]
        splittedcontent = splittedcontent[:(len(splittedcontent)-1)]
        jokes = jokes + splittedcontent
        offset = offset + 4
        
    else:
        run = False
chrome_options = Options()
chrome_options.add_argument("user-data-dir=" + os.path.dirname(sys.argv[0]))
driver = webdriver.Chrome(os.path.dirname(os.path.realpath(sys.argv[0])) + '\\chromedriver.exe', chrome_options=chrome_options)
driver.maximize_window()
driver.get("https://web.whatsapp.com")
time.sleep(25)
bot_users = {} # A dictionary that stores all the users that sent activate bot
browser = driver
while True:
    unread = browser.find_elements_by_class_name("OUeyt") # The green dot tells us that the message is new
    name,message  = '',''
    if len(unread) > 0:
        ele = unread[-1]
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(ele, 0, -20) # move a bit to the left from the green dot

    # Clicking couple of times because sometimes whatsapp web responds after two clicks
        try:
            action.click()
            action.perform()
            action.click()
            action.perform()
        except Exception as e:
            pass
        try:
            name = browser.find_element_by_class_name("_2zCDG").text  # Contact name
            message = browser.find_elements_by_class_name("vW7d1")[-1]  # the message content
            print(message.text)
            if 'הפעל בוט' in message.text.lower():
                if name not in bot_users:
                    bot_users[name] = True
                    text_box = browser.find_element_by_class_name("_2S1VP")
                    response = "שלום "+name+". הבוט הופעל!"
                    text_box.send_keys(response)
                    text_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    text_box.send_keys("פקודות אפשריות:")
                    text_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    text_box.send_keys("'הפעל בוט'")
                    text_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    text_box.send_keys("'בדיחה'")
                    text_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    text_box.send_keys("'כבה בוט'\n")
                    
                    GoToEmptyGroup()
            elif name in bot_users:
                if 'בדיחה' in message.text.lower():
                    #getNews()
                    randpage = random.randint(0,len(jokes))
                    page = jokes[randpage]
                    text_box = browser.find_element_by_class_name("_2S1VP")
                    response = "קבלו בדיחה:\n"
                    text_box.send_keys(response)
                    response2 = ""
                    for x in page:
                        response2 = response2 + " " + x
                    text_box.send_keys(response2 + "\n")
                    GoToEmptyGroup()
                elif 'כבה בוט' in message.text.lower():
                    
                    text_box = browser.find_element_by_class_name("_2S1VP")
                    response = "Bye "+name+".\n"
                    text_box.send_keys(response)
                    GoToEmptyGroup()
                    del bot_users[name]
                else:
                    
                    GoToEmptyGroup()
            else:
                GoToEmptyGroup()
        except Exception as e:
            print(e)
            pass
    time.sleep(0.5) # A 2 second pause so that the program doesn't run too fast
#def DetectNothingFound(pagecontent):
#    #blabla

'''soup2 = BeautifulSoup("""
<div><div>blabla></div>shasha</div><div>kuku</div>
""", 'lxml')
divs = soup2.find_all('div')'''

