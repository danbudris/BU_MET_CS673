from selenium.webdriver.common.keys import Keys
import base_testcase


class LoginTestCase(base_testcase.CommonLiveServerTestCase):

    def test_login(self):
        # This script verify registered user login on communication web page

        self.driver.get("http://127.0.0.1:8000/communication")
        self.driver.find_element_by_id("username").send_keys(self.user_name)
        self.driver.find_element_by_id("password").send_keys(self.user_pw)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        self.pause()

        
