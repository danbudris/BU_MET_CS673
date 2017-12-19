"""A common base test case for re-using."""

import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.testcases import LiveServerTestCase
from selenium import webdriver

from issue_tracker import utils


class CommonLiveServerTestCase(StaticLiveServerTestCase):
    """Common methods for all tests."""

    DEFAULT_PAUSE_TIME = 5

    def setUp(self):

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.user_name = 'username'
        self.user_pw = 'usernamepw'
        utils.create_user(first='Jane',
                          last='Doe',
                          username=self.user_name)
        self.super_user_name = 'test'
        self.super_user_pw = 'testpw'
        utils.create_super_user(first='Super',
                                last='Woman',
                                username=self.super_user_name)
        utils.create_users(users=utils.USERS)
        utils.create_projects(number_of_projects=5)
        utils.create_issues(number_of_issues=10)

    def tearDown(self):
        self.driver.quit()
        utils.wipe_db()

    def pause(self, seconds=None):
        """Time to pause between clicks.

        Args:
          seconds: The number of seconds to pause.
        """
        if seconds:
            time.sleep(seconds)
        else:
            time.sleep(self.DEFAULT_PAUSE_TIME)
