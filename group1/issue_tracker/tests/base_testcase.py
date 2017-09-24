"""A common base test case for re-using."""

import time

from django.test.testcases import LiveServerTestCase
from selenium import webdriver

from app import utils


class CommonLiveServerTestCase(LiveServerTestCase):
    """Common methods for all tests."""

    DEFAULT_PAUSE_TIME = 0.25

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.user_name = 'username'
        self.user_pw = '%spw' % self.user_name
        utils.create_user(first='Jane',
                          last='Doe',
                          username=self.user_name)
        self.super_user_name = 'superuser'
        self.super_user_pw = '%spw' % self.super_user_name
        utils.create_super_user(first='Super',
                                last='Woman',
                                username=self.super_user_name)
        utils.create_users(users=utils.USERS)
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
