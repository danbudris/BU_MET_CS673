"""A common base test case for re-using."""

import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.testcases import LiveServerTestCase
from selenium import webdriver

from issue_tracker import utils
from comm import models


class CommonLiveServerTestCase(StaticLiveServerTestCase):
    """Common methods for all tests."""

    DEFAULT_PAUSE_TIME = 5

    def setUp(self):
        self.profile = webdriver.FirefoxProfile()
        self.profile.DEFAULT_PREFERENCES['frozen']["media.navigator.permission.disabled"] = True
        self.driver = webdriver.Firefox(firefox_profile=self.profile)
        #self.driver =  webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.user_name = 'username'
        self.user_pw = 'usernamepw'
        utils.create_user(first='Jane',
                          last='Doe',
                          username=self.user_name)
        self.super_user_name = 'leia'
        self.super_user_pw = 'leiapw'
        utils.create_super_user(first='leia',
                                last='organa',
                                username=self.super_user_name)
        utils.create_users(users=utils.USERS)
        utils.create_projects(number_of_projects=2)


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
