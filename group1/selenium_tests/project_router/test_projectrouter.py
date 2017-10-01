from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys


class TestProjectRouter(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
        self.base_url = "http://127.0.0.1:8000"

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_project_and_create_issue(self):
        # User has heard about a new online PM app. They go
        # to check out its homepage
        self.browser.get(self.base_url)

        # They notice the page title and header mention Project
        self.assertIn('Project', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Project', header_text)
