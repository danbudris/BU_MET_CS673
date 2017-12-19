import unittest
from selenium.webdriver.common.keys import Keys
import base_testcase

class EditTeamTestCase(base_testcase.CommonLiveServerTestCase):


    def test_edit_team(self):
        # Aim of this script is that edit team name
        # User login and create a team which name is "test room 3".
        #and edit team name and check it.

        self.driver.get('http://127.0.0.1:8000/communication')
        self.driver.find_element_by_id('username').send_keys(
            self.super_user_name)
        self.driver.find_element_by_id('password').send_keys(
            self.super_user_pw)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        self.pause(2)
        self.driver.find_element_by_partial_link_text('Create New Teams').click()
        self.pause(2)
        self.driver.find_element_by_id('teamname').send_keys('test room 3')
        self.driver.find_element_by_id('saveTeam').click()
        self.driver.find_element_by_id('text').send_keys('in a galaxy far, far away')
        self.driver.find_element_by_id('sendcleartext').click()
        self.driver.find_element_by_id('dropdownMenu1').click()
        self.driver.find_element_by_link_text('Edit Team').click()
        self.driver.find_element_by_id('teamname').clear()
        self.driver.find_element_by_id('teamname').send_keys('editted')
        self.driver.find_element_by_id('saveTeam').click()
        element = self.driver.find_element_by_partial_link_text('editted').text
        assert "editted" in element
        self.pause()
