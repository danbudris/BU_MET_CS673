from selenium.webdriver.common.keys import Keys
import base_testcase
from selenium import webdriver


class CreateRoomTestCase(base_testcase.CommonLiveServerTestCase):

    def test_create_team(self):
        # This script creates a new chat team in communication application.
        # user login and create a team which name is "test room".

        self.driver.get('http://127.0.0.1:8000/communication')
        self.driver.find_element_by_id('username').send_keys(
            self.user_name)
        self.driver.find_element_by_id('password').send_keys(
            self.user_pw)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        self.pause(2)
        self.driver.find_element_by_partial_link_text('Create New Teams').click()
        self.pause(2)
        self.driver.find_element_by_id('teamname').send_keys('test room')
        self.driver.find_element_by_id('saveTeam').click()
        element = self.driver.find_elements_by_id('room-list')
        self.assertTrue(len(element));
        
