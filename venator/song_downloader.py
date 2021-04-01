#https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver
#https://stackoverflow.com/questions/8871654/how-to-press-click-the-button-using-selenium-if-the-button-does-not-have-the-id

# let's do something where we save cookies after each session (might be some backend checks there)


'''
SETUP
- open a new empty session and save the cookies to cookies.pkl
- seleniumwire ,mitmproxy and selenium + geckodriver 
'''

import os
import json
import time
import pickle
import random
import requests
from seleniumwire import webdriver
from pyvirtualdisplay import Display
from config.redis_conn import redis_conn

class SongDownloader():
    def __init__(self):
        
        # start virtual display for selenium
        # https://github.com/dimmg/dockselpy
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

        self.browser = webdriver.Firefox(seleniumwire_options = {
            'backend': 'mitmproxy'
        })

        self.song_dir_path = os.getenv("SONG_DIR_PATH")
        self.browser.get('https://play.anghami.com/') # can't set cookies in an empty document
        self.current_cookie_jar = False

    def _set_cookies(self,cookie_jar):

        # remove the .inuse from the old jar
        if self.current_cookie_jar:
            os.rename(self.current_cookie_jar+'.inuse',self.current_cookie_jar)
            
        try:
            cookies = pickle.load(open(cookie_jar, "rb"))
        except IOError:
            raise BaseException("Couldn't find cookie jar: "+cookie_jar)

        for cookie in cookies:
            self.browser.add_cookie(cookie)
        
        # add an inuse to the new one. since 2 workers can't share the same cookie jar at the same time
        os.rename(cookie_jar,cookie_jar+'.inuse')
        self.current_cookie_jar = cookie_jar

    def _pick_cookie_jar(self):
        '''
        Pick a new cookie jar for us to use with each request
        '''
        all_cookie_jars = os.listdir("config/secrets") 
        free_cookie_jars = [os.path.join("config/secrets",i) for i in all_cookie_jars if i.endswith(".pkl")]
        return random.choice(free_cookie_jars)
 
    # gotta refresh after setting the cookies 
    def _press_play_and_get_MediaLink(self):
        while True:
            try:
                time.sleep(2) # refresh the element reference everytime 
                button = self.browser.find_element_by_xpath("/html/body/anghami-root/anghami-base/div[1]/div/div/anghami-view/div/div[1]/anghami-collection-header-side/div/div/anghami-collection-header-buttons/div/button[1]") 
                button.click()
                print("CLICK")
                time.sleep(2)
                mediaURL = self.did_media_request()
                if mediaURL: # did anghami do the media request?
                    return mediaURL
            except Exception as e:
                print(e)

    def did_media_request(self):
        for request in self.browser.requests:
            # it also comes from this cloudfront domain if nothing else works: d3nhk3h83d1umo.cloudfront.net
            if request.response and request.response.status_code==206 and request.response.headers['Content-Type']=='video/mp4':
                return request.url
        return False
    
    def _getSongIDFromURL(self,song_url): # used internally to keep track of different songs and stuff 
        return song_url.split('/')[4]

    def _download_media(self,media_url,song_url):
        song_media_bytes = requests.get(media_url).content
        full_song_path = os.path.join(self.song_dir_path,'Anghami_'+self._getSongIDFromURL(song_url)+'.mp3')
        open(full_song_path,'wb+').write(song_media_bytes)
        return True

    def download_song(self,song_url): # todo: checks to see if we already downloaded a songs and checks to remove the least downloaded one if it gets too tight
        
        self._set_cookies(self._pick_cookie_jar()) 

        self.browser.get(song_url)
        media_url = self._press_play_and_get_MediaLink()
        self._download_media(media_url,song_url)

        redis_conn.publish('downloaded_songs',json.dumps({
            "song_media_name":'Anghami_'+self._getSongIDFromURL(song_url)+'.mp3',
            "song_id":self._getSongIDFromURL(song_url)
        }))
        # todo save how many times a song was requested in redis
        return True