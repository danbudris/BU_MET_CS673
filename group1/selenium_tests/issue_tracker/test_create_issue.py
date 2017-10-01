from selenium.webdriver.common.keys import Keys
import base_testcase


class CreateIssueTestCase(base_testcase.CommonLiveServerTestCase):
    """Tests for the create issue page."""

    def create_issue(self, with_title=True):
        """Common test paths for the create issue page tests.

        Arg:
          with_title: boolean for determine whether to populate a title.
        """
        self.driver.get('http://127.0.0.1:8000/issue_tracker/issue/create')
        self.driver.find_element_by_id('username').send_keys(
            self.super_user_name)
        self.driver.find_element_by_id('password').send_keys(
            self.super_user_pw)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        self.pause()
        self.driver.get('http://127.0.0.1:8000/issue_tracker/issue/create')
        self.pause()
        self.driver.find_element_by_xpath(
            "//*[@name='project']/option[2]").click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_issue_type"]/option[2]').click()
        if with_title:
            self.driver.find_element_by_id('id_title').send_keys(
                'Sample Title')
        self.driver.find_element_by_id('id_description').send_keys(
            'Luke, I am your father')
        self.driver.find_element_by_xpath(
            '//*[@id="id_priority"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_assignee"]/option[2]').click()
        self.driver.find_element_by_css_selector(
            '.btn-primary[value="Create"]').click()
        self.pause()

    def test_create_issue(self):
        """Positive test case for creating a new issue."""
        self.create_issue(with_title=True)
        assert "http://127.0.0.1:8000/issue_tracker/issue/view/" in self.driver.current_url

    def test_create_issue_validation(self):
        """Create an invalid issue without a title."""
        self.create_issue(with_title=False)
        self.assertTrue(self.driver.find_element_by_class_name(
            'errorlist').is_displayed())
