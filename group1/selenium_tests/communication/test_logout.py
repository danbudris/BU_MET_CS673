from selenium.webdriver.common.keys import Keys
import base_testcase


class LogoutTestCase(base_testcase.CommonLiveServerTestCase):

    def test_logout(self):
        # This script check to logout

        self.driver.get("http://127.0.0.1:8000/communication")
        self.driver.find_element_by_id("username").send_keys(self.user_name)
        self.driver.find_element_by_id("password").send_keys(self.user_pw)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        self.pause()
        self.driver.find_element_by_id("id_username_link").click()
        self.driver.find_element_by_partial_link_text("Logout").click()
