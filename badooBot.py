from selenium import webdriver
from time import sleep

from secret import username, password
class BadooBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get('https://badoo.com/uk/mobile/')

        sleep(2)

        fb_btn = self.driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/div/a[2]')
        fb_btn.click()

        fb_btn = self.driver.find_element_by_xpath('//*[@id="page"]/div[2]/div[3]/section/div/div/div[3]/div/div[1]/a')
        fb_btn.click()

        # switch to login popup
        base_window = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        login_btn.click()

        self.driver.switch_to_window(base_window)

        sleep(5)

        # popup_1 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]/span')
        # popup_1.click()
        #
        # sleep(1)
        #
        # popup_2 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        # popup_2.click()

    def like(self):
        like_btn = self.driver.find_element_by_xpath('//*[@id="mm_cc"]/div[1]/section/div/div[2]/div/div[2]/div[1]/div[1]')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]')
        dislike_btn.click()

    def auto_swipe(self):
        while True:
            sleep(0.25)
            try:
                self.like()
            except Exception:
                try:
                    self.close_popup()
                except Exception:
                    self.close_match()

    def close_popup(self):
        sleep(1)
        pw_in = self.driver.find_element_by_xpath('/html/body/aside/section/div[1]/div/div[1]/div[3]/form/div/div[1]/div/input')
        pw_in.send_keys("Хай!)")
        popup_3 = self.driver.find_element_by_xpath('/html/body/aside/section/div[1]/div/div[1]/div[3]/form/div/div[2]/div')
        popup_3.click()

    def close_match(self):
        sleep(1)
        try:
            match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
            match_popup.click()
            return
        except:
            pass

        try:
            match_popup = self.driver.find_element_by_xpath('/html/body/aside/section/div[1]/div/div[2]/div/div[1]')
            match_popup.click()
            return
        except:
            pass

        try:
            sleep(0)
            match_popup = self.driver.find_element_by_xpath('/html/body/aside/section/div[1]/div/div[2]/i')
            match_popup.click()
            return
        except:
            pass

