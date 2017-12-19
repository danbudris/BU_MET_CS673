from selenium.webdriver.common.keys import Keys
import base_testcase
from selenium import webdriver

class DialogTestCase(base_testcase.CommonLiveServerTestCase):


    def test_dialog(self):
        # Aim of this script is that check functionality of dialog in a chat room.
        # Firstly, user login and create a team which name is "test room 4".
        # and then send a message to this room and another user also send a
        #message to same room and test checks if messages are sent.

        self.driver.get('http://127.0.0.1:8000/communication')
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
        self.driver.find_element_by_id('text').send_keys('hello')
        self.driver.find_element_by_id('sendcleartext').click()
        self.pause()
        #second user
        driver2 = webdriver.Firefox()
        driver2.get('http://127.0.0.1:8000/communication');
        driver2.set_window_size(700, 1000)
        driver2.set_window_position(700, 0)
        driver2.find_element_by_id("username").send_keys(self.super_user_name)
        driver2.find_element_by_id("password").send_keys(self.super_user_pw)
        driver2.find_element_by_id("password").send_keys(Keys.ENTER)
        self.pause()
        driver2.find_element_by_id('text').send_keys('hi! whats up')
        driver2.find_element_by_id('sendcleartext').click()
        element = driver2.find_element_by_class_name('messagecontent').text
        assert "hi! whats up" and "hello" in element
        driver2.quit()
