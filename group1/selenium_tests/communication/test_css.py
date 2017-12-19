from selenium.webdriver.common.keys import Keys
import base_testcase

class UnsanitizedMessageTestCase(base_testcase.CommonLiveServerTestCase):


    def unsanitized_message(self):
        # Aim of this script is that unsanitized message is rendered as a text in the chat room.
        # Firstly, user login and create a team which name is "test room 3".
        # and then send a message to this room and check if it is sent as a text.

        self.driver.get('http://127.0.0.1:8000/communication')
        self.driver.find_element_by_id('username').send_keys(
            self.user_name)
        self.driver.find_element_by_id('password').send_keys(
            self.user_pw)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        self.pause(2)
        self.driver.find_element_by_partial_link_text('Create New Teams').click()
        self.pause(2)
        self.driver.find_element_by_id('teamname').send_keys('test room 3')
        self.driver.find_element_by_id('saveTeam').click()
        self.pause(2)
        self.driver.find_element_by_id('text').send_keys('<button type="button" >')
        self.pause(2)
        self.driver.find_element_by_id('sendcleartext').click()
        self.pause(2)
        element = self.driver.find_element_by_class_name('messagecontent').text
        assert 'button type' in element
