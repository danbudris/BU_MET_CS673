from selenium.webdriver.common.keys import Keys
import base_testcase


class LoginTestCase(base_testcase.CommonLiveServerTestCase):

    def test_login(self):
        """Verify login for a normal user works."""
        self.driver.get("http://127.0.0.1:8000/issue_tracker/issue/create")
        self.driver.find_element_by_id("username").send_keys(self.user_name)
        self.driver.find_element_by_id("password").send_keys(self.user_pw)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        self.pause()
