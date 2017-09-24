from selenium.webdriver.common.keys import Keys
from app.tests import base_testcase


class TestSideBar(base_testcase.CommonLiveServerTestCase):

    def test_sidebar(self):
        """Test the sidebar elements are all present."""

        self.driver.get("localhost:8081/issue/create")
        self.driver.find_element_by_id("id_username").send_keys(
            self.super_user_name)
        self.driver.find_element_by_id("id_password").send_keys(
            self.super_user_pw)
        self.driver.find_element_by_id("id_password").send_keys(Keys.ENTER)
        self.pause()
        self.driver.find_element_by_xpath('//*[@href="/"]').click()
        self.pause()
        self.driver.find_element_by_xpath('//*[@href="/admin/login/"]').click()
        self.pause()
        # Currently, the admin site changes to django admin site. This has no
        # links to point back to the originating page.
        self.driver.get("localhost:8081/")
        self.driver.find_element_by_xpath('//*[@href="/issue/create"]').click()
        self.pause()
        self.driver.find_element_by_xpath('//*[@href="/"]').click()
        self.pause()
        self.driver.find_element_by_xpath('//*[@href="/issue/search"]').click()
        self.pause()
