# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re


class TestLoginFail(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_login_fail(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("invaliduser")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("invalidpass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "Username or Password is incorrect ! Please try again !",
            driver.find_element_by_css_selector("div.alert.alert-danger").text)

    def test_login_pass(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "admin",
            driver.find_element_by_link_text("admin").text)
        driver.find_element_by_link_text("admin").click()
        driver.find_element_by_link_text("Logout").click()

    def test_logout(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("admin").click()
        driver.find_element_by_link_text("Logout").click()
        self.assertEqual(
            "Thank you and Good bye !!",
            driver.find_element_by_css_selector("h1.page-header").text)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
