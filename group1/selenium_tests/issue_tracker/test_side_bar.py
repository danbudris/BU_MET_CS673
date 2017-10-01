from selenium.webdriver.common.keys import Keys
import base_testcase


class TestSideBar(base_testcase.CommonLiveServerTestCase):

    def test_sidebar(self):
        """Test the sidebar elements are all present."""

        self.driver.get('http://127.0.0.1:8000/issue_tracker/issue/create')
        self.driver.find_element_by_id('username').send_keys(
            self.super_user_name)
        self.driver.find_element_by_id('password').send_keys(
            self.super_user_pw)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        self.pause()
        self.driver.get('http://127.0.0.1:8000/issue_tracker/issue/create')
        # Currently, the admin site changes to django admin site. This has no
        # links to point back to the originating page.
        self.driver.get("http://127.0.0.1:8000/issue_tracker/")
        self.driver.find_element_by_xpath('//*[@href="/issue_tracker/issue/create"]').click()
        self.pause()
        self.pause()
        self.driver.find_element_by_xpath('//*[@href="/issue_tracker/issue/search"]').click()
        self.pause()

