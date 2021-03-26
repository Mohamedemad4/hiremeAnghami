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
from seleniumwire import webdriver

browser = webdriver.Firefox(seleniumwire_options = {
    'backend': 'mitmproxy'
})


browser.get('https://play.anghami.com/') # can't set cookies in an empty document

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
            if didMediaRequest(): # did anghami do the media request?
                break
        except Exception as e:
            print(e)

def didMediaRequest():
    for request in browser.requests:
        # it also comes from this cloudfront domain if nothing else works: d3nhk3h83d1umo.cloudfront.net
        if request.response and request.response.status_code==206 and request.response.headers['Content-Type']=='video/mp4':
            print(request.url)
            return True
    return False

PlayAndGetMediaLink()
