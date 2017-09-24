from selenium.webdriver.common.keys import Keys
from app.tests import base_testcase
import unittest


class CreateIssueTestCase(base_testcase.CommonLiveServerTestCase):
    @unittest.skip("edit issue button currently not working")
    def test_edit_issue(self):

        # For this to work we need to either run a script to create generic
        # issues, or create an issue to view as part of the test.  Currently
        # creating dynamically, but there's a better way to do this when we
        # have time using mocks or a script

        self.driver.get('localhost:8081/issue/create')
        self.driver.find_element_by_id(
            'id_username').send_keys(self.super_user_name)
        self.driver.find_element_by_id(
            'id_password').send_keys(self.super_user_pw)
        self.driver.find_element_by_id('id_password').send_keys(Keys.ENTER)
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

        # save a value
        title = self.driver.find_element_by_css_selector(
            '#page-inner > div:nth-child(1) > h1:nth-child(1)').text
        # click on edit issue.
        self.driver.find_element_by_css_selector(
            'button.btn').click()
        self.pause()
        # edit a value
        self.driver.find_element_by_id('id_title').send_keys('blarg')
        # save changes
        self.driver.find_element_by_css_selector('.btn-primary')
        # check value changed
        self.assertNotEqual(
            title,
            self.driver.find_element_by_class_name('bug_name').text)

    @unittest.skip('To be built once edit feature is resolved')
    def test_edit_access(self):
        # this test is not active, but should ensure we can only reach edit
        # page when an issue is selected
        return
