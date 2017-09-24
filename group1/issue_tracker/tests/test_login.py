from selenium.webdriver.common.keys import Keys
from app.tests import base_testcase


class LoginTestCase(base_testcase.CommonLiveServerTestCase):

    def test_login(self):
        """Verify login for a normal user works."""
        self.driver.get("localhost:8081/issue/create")
        self.driver.find_element_by_id("id_username").send_keys(self.user_name)
        self.driver.find_element_by_id("id_password").send_keys(self.user_pw)
        self.driver.find_element_by_id("id_password").send_keys(Keys.ENTER)
        self.pause()
