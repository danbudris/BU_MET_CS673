from selenium.webdriver.common.keys import Keys
import base_testcase


class ViewIssueTestCase(base_testcase.CommonLiveServerTestCase):

    def test_view_issue(self):
        # for this to work we need to either run a script to create generic
        # issues, or create an issue to view as part of the test.  Currently
        # creating dynamically, but there's a better way to do this when we
        # have time using mocks or a script

        self.driver.get('http://127.0.0.1:8000/issue_tracker/issue/create')
        self.driver.find_element_by_id('username').send_keys(
            self.super_user_name)
        self.driver.find_element_by_id('password').send_keys(
            self.super_user_pw)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        self.pause()
        self.driver.find_element_by_xpath(
            '//*[@id="id_project"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_issue_type"]/option[2]').click()
        self.driver.find_element_by_id('id_title').send_keys('Sample Title')
        self.driver.find_element_by_id('id_description').send_keys(
            'Luke, I am your father')
        self.driver.find_element_by_xpath(
            '//*[@id="id_priority"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_assignee"]/option[2]').click()
        self.driver.find_element_by_css_selector(
            '.btn-primary[value="Create"]').click()

        # The above code just creates an issue, the following is where
        # our test begins

        self.driver.get('http://127.0.0.1:8000/issue_tracker')
        self.pause()
        first_issue = self.driver.find_element_by_css_selector(
            '#page-wrapper > table:nth-child(2) > tbody:nth-child(2) > '
            'tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
        first_issue.click()
        self.pause()
