from selenium import webdriver
from time import sleep
from utils import waitFor, lateGet
import re
from secret import username, password
from selenium.webdriver.common.keys import Keys
from memo.url_memo import memo
from common import DEFAULT_URL_DATA
from image_loader import downloadimg
import random

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get('https://tinder.com')

        # fb_btn = lateGet(lambda: self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button'), 5)
        # if fb_btn != None:
        #     print("sdtsts")
        #     sleep(10)
        #     fb_btn.click()
        fb_btn = lateGet(lambda: self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button'))
        fb_btn.click()

        # switch to login popup
        base_window = self.driver.window_handles[0]

        waitFor(lambda: self.driver.window_handles[1])

        self.driver.switch_to_window(self.driver.window_handles[1])

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        login_btn.click()

        self.driver.switch_to_window(base_window)

        popup_1 = lateGet(lambda: self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]/span'))
        popup_1.click()

        popup_2 = lateGet(lambda: self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]'))
        popup_2.click()

        waitFor(lambda: self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]'))

        sleep(4)

    def like(self):
        def _like():
            urls = self.getCurrentFaceURLs()
            for url in urls:
                memo.upd_urls({url: DEFAULT_URL_DATA})

            like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
            dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
            if random.random() > 0.5:
                like_btn.click()
            else:
                dislike_btn.click()

        try:
            _like()
        except:
            try:
                self.close_popup()
                _like()
            except:
                self.close_match()
                _like()


    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]')
        dislike_btn.click()

    def auto_swipe(self):
        while True:
            self.like()
            sleep(0.3)


    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def getCurrentFaceURLs(self):

        def getUrl(index):
            div = self.driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[' + str(index) + ']')

            html = div.get_attribute('innerHTML')
            url = re.search(r'quot;(\S+)&quot', html).group(1)

            root = self.driver.find_element_by_xpath('//*[@id="Tinder"]/body')
            root.send_keys(Keys.SPACE)

            return url

        res = []
        indx = 1
        while True:
            try:
                res += [getUrl(indx)]
                indx += 1
                sleep(0.2)
            except:
                return res
