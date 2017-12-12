from selenium.webdriver.common.keys import Keys
import base_testcase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class GoogleDriveUploadTestCase(base_testcase.CommonLiveServerTestCase):


    def test_upload(self):
        # Aim of this script is that check functionality of google drive upload file in a chat room.

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
        self.driver.find_element_by_id('teamname').send_keys('test room 8')
        self.driver.find_element_by_id('saveTeam').click()
        self.pause(1)
        #current window
        window_before = self.driver.window_handles[0]
        # click on the link that opens a new window
        self.driver.find_element_by_id('google drive').click()
        self.driver.find_element_by_partial_link_text('Upload File').click()
        self.pause()
        #get the window handle after a new window has opened
        window_after = self.driver.window_handles[1]
        #switch on to new child window
        self.driver.switch_to.window(window_after)
        # login in the popup
        self.driver.find_element_by_id('identifierId').send_keys('cs673.test@gmail.com')
        self.pause(2)
        self.driver.find_element_by_id('identifierNext').click()
        self.pause(2)
        self.driver.find_element_by_id('password').send_keys('123cs673')
        self.pause(2)
        self.driver.find_element_by_id('passwordNext').click()
        #switch back to original window
        self.driver.switch_to.window(window_before)
        #since the pop-up is now in an iframe
        #self.driver.switch_to.frame(3)
        #self.driver.find_element_by_partial_link_text('Select a file from your computer').send_keys(".\myfile.txt")
