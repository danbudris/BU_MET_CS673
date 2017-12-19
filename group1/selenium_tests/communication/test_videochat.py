from selenium.webdriver.common.keys import Keys
import base_testcase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class VideoChatTestCase(base_testcase.CommonLiveServerTestCase):


    def test_videochat(self):
        # Aim of this script is that check functionality of video chat in a chat room.

        self.driver.get('http://localhost:8000/communication')
        self.driver.set_window_size(700, 1000)
        self.driver.set_window_position(0, 0)
        self.driver.find_element_by_id('username').send_keys(
            self.user_name)
        self.driver.find_element_by_id('password').send_keys(
            self.user_pw)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        self.pause(2)
        self.driver.find_element_by_partial_link_text('Create New Teams').click()
        self.pause(2)
        self.driver.find_element_by_id('teamname').send_keys('test room 4')
        self.driver.find_element_by_id('saveTeam').click()
        self.pause(1)
        self.driver.find_element_by_id('startVideo').click()
        self.pause()

        #second user
        driver2 = webdriver.Firefox(firefox_profile=self.profile)
        driver2.get('http://127.0.0.1:8000/communication');
        driver2.set_window_size(700, 1000)
        driver2.set_window_position(700, 0)
        driver2.find_element_by_id("username").send_keys(self.super_user_name)
        driver2.find_element_by_id("password").send_keys(self.super_user_pw)
        driver2.find_element_by_id("password").send_keys(Keys.ENTER)
        self.pause()
        driver2.find_element_by_id('startVideo').click()
        self.pause()
        driver2.quit()
