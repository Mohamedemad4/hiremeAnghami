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
from selenium.common.exceptions import TimeoutException

class SongDownloader():
    def __init__(self,worker_id):
        
        # start virtual display for selenium
        # https://github.com/dimmg/dockselpy
        self.display = Display(visible=0, size=(1280,1024))
        self.display.start()

        self.browser = webdriver.Firefox(seleniumwire_options = {
            'backend': 'mitmproxy'
        })

        self.browser.request_interceptor = self._sw_interceptor

        self.song_dir_path = os.getenv("SONG_DIR_PATH")
        self.browser.get('https://play.anghami.com/') # can't set cookies in an empty document
        self.current_cookie_jar = False

        self.worker_id = worker_id

        redis_conn.set(self.worker_id,"") # reset it form failed jobs or whatever so the "net" is empty and the interceptor can catch fresh stuff

    def _sw_interceptor(self,request):
        if 'cloudfront' in request.url and 'Key-Pair-Id' in request.url:
            redis_conn.set(self.worker_id,request.url)

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
                print("clicked play")
                try:
                    mediaURL = self.browser.wait_for_request('.*m4a\?.*',timeout=5)
                    return mediaURL
                except TimeoutException:
                    print("timed out clicking play again")
                    for r in self.browser.requests: # try looking at the request history
                        if r.response: # for sent requests that aren't back yet
                            if r.response.headers['Content-Type']=='video/mp4':
                                return r.url
                    
                    # if this doesn't work check if the interceptor caught anything
                    ## out of these 3 one usually works!
                    temp = redis_conn.get(self.worker_id)

                    if temp: 
                        redis_conn.set(self.worker_id,"")
                        return temp

            except Exception as e:
                print(e)
    
    def _getSongIDFromURL(self,song_url): # used internally to keep track of different songs and stuff 
        return song_url.split('/')[4]

    def _download_media(self,media_url,song_url):
        song_media_bytes = requests.get(media_url).content
        full_song_path_mp4 = os.path.join(self.song_dir_path,'Anghami_'+self._getSongIDFromURL(song_url)+'.mp4')
        open(full_song_path_mp4,'wb+').write(song_media_bytes)

        # convert mp4 to mp3 and remove the mp4 file
        os.system("ffmpeg -i {0} {1}".format( 
            full_song_path_mp4,
            full_song_path_mp4.replace('mp4','mp3')
        ))
        os.remove(full_song_path_mp4)

        return True

    def _press_pause(self):
        print("got link pausing playback")
        button = self.browser.find_element_by_xpath("/html/body/anghami-root/anghami-base/div[1]/anghami-player/div[2]/div/div[2]/div/div/div/div")
        button.click()

    def download_song(self,song_url):
        if not 'Anghami_'+self._getSongIDFromURL(song_url)+'.mp3' in os.listdir(self.song_dir_path): # checks to see if we already have the song downloaded
            self._set_cookies(self._pick_cookie_jar()) 

            self.browser.get(song_url)
            media_url = self._press_play_and_get_MediaLink()
            self._press_pause()
            self._download_media(media_url,song_url)

        redis_conn.publish('downloaded_songs',json.dumps({
            "song_media_name":'Anghami_'+self._getSongIDFromURL(song_url)+'.mp3',
            "song_id":self._getSongIDFromURL(song_url)
        }))

        return True