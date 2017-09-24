import unittest
from selenium.webdriver.common.keys import Keys
from app.tests import base_testcase


class SearchIssuesTestCase(base_testcase.CommonLiveServerTestCase):
    """Tests for the search issues page."""

    def create_testable_issue(self):
        self.driver.get('localhost:8081/issue/create')
        self.driver.find_element_by_id('id_username').send_keys(
            self.super_user_name)
        self.driver.find_element_by_id('id_password').send_keys(
            self.super_user_pw)
        self.driver.find_element_by_id('id_password').send_keys(Keys.ENTER)
        self.pause()
        self.driver.find_element_by_xpath(
            '//*[@id="id_project"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_issue_type"]/option[2]').click()
        self.driver.find_element_by_id('id_title').send_keys(
            'Searchable Title')
        self.driver.find_element_by_id('id_description').send_keys(
            "These aren't the droids you're looking for")
        self.driver.find_element_by_xpath(
            '//*[@id="id_priority"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_assignee"]/option[2]').click()
        self.driver.find_element_by_css_selector(
            '.btn-primary[value="Create"]').click()

    def test_search_single_field(self):
        """Common use cases for the search page"""

        self.create_testable_issue()
        destination = self.driver.current_url
        # goes to the search page
        self.driver.find_element_by_css_selector(
            '#main-menu > li:nth-child(6) > a:nth-child(1)').click()
        self.pause()
        # searches on title field
        self.driver.find_element_by_id('id_title').send_keys('Searchable')
        self.driver.find_element_by_css_selector(
            '.btn-primary').click()
        self.pause()
        title = self.driver.find_element_by_css_selector(
            '#page-wrapper > table:nth-child(2) > tbody:nth-child(2) > '
            'tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
        self.assertEqual(title.text, 'Searchable Title')
        title.click()
        self.pause()
        assert self.driver.current_url == destination

    @unittest.skip('Currently this is broken, when we have validation setup on'
                   ' this page we will fix the test')
    def test_search_empty_forms(self):
        return

    def test_search_multiple_fields(self):
        self.create_testable_issue()
        destination = self.driver.current_url

        self.pause()
        self.driver.find_element_by_css_selector(
            '#main-menu > li:nth-child(6) > a:nth-child(1)').click()

        self.driver.find_element_by_css_selector('#id_priority').click()
        self.driver.find_element_by_css_selector(
            '#id_priority > option:nth-child(3)').click()
        self.pause()
        self.driver.find_element_by_css_selector(
            '#id_description').send_keys('droids')
        self.driver.find_element_by_css_selector(
            '.btn-primary').click()
        self.pause()
        title = self.driver.find_element_by_css_selector(
            '#page-wrapper > table:nth-child(2) > tbody:nth-child(2) > '
            'tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
        self.assertEqual(title.text, 'Searchable Title')
        title.click()
        self.pause()
        self.assertEqual(self.driver.current_url, destination)
