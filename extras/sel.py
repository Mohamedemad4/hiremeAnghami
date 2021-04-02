#https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver
#https://stackoverflow.com/questions/8871654/how-to-press-click-the-button-using-selenium-if-the-button-does-not-have-the-id

# let's do something where we save cookies after each session (might be some backend checks there)


'''
SETUP
- open a new empty session and save the cookies to cookies.pkl
- seleniumwire ,mitmproxy and selenium + geckodriver 
'''

import pickle
import time
import sys
from seleniumwire import webdriver
from selenium.common.exceptions import TimeoutException
browser = webdriver.Firefox(seleniumwire_options = {
    'backend': 'mitmproxy'
})


browser.get('https://play.anghami.com/') # can't set cookies in an empty document

if len(sys.argv)==2:
    input("Capture Cookies\n[PRESS ENTER]\n")
    pickle.dump( browser.get_cookies() , open("cookies_"+sys.argv[1]+"_.pkl","wb+"))
    exit()

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

# gotta refresh after setting the cookies 
browser.get('https://play.anghami.com/song/25770989')

def PlayAndGetMediaLink():
    while True:
        try:
            time.sleep(2) # refresh the element refrence everytime 
            button = browser.find_element_by_xpath("/html/body/anghami-root/anghami-base/div[1]/div/div/anghami-view/div/div[1]/anghami-collection-header-side/div/div/anghami-collection-header-buttons/div/button[1]") 
            button.click()
            print("CLICK")
            time.sleep(2)
            try:
                r = browser.wait_for_request('.*m4a\?.*',timeout=5)
                print(r)
                break
            except TimeoutException:
                print("TImED OUT")
        except Exception as e:
            print(e)

PlayAndGetMediaLink()
