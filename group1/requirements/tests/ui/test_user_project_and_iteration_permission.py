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


class TestUserProjectAndIterationPermission(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_user_project_and_iteration_permission(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("george")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("george").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Return to Home").click()
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("SamuelLJackson")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("snakes")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath(
            "//a[@onclick=\"showDialog('/req/newproject');\"]").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_title"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("New Project")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            "This project shows that only a project manager permission will allow a user to make projects and iterations and add users to the project.  Samuel L Jackson has this permission.  George does not.")
        driver.find_element_by_link_text("Create Project").click()
        driver.find_element_by_link_text("Open").click()
        driver.find_element_by_xpath(
            "//div[@id='page-wrapper']/div[2]/div[2]/div/div/div/h2/a[2]/i").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_user_role"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        Select(driver.find_element_by_id("id_user_role")).select_by_visible_text(
            "Developer")
        driver.find_element_by_xpath(
            "//a[contains(@data-user-name, 'george')]").click()
        time.sleep(1)
        driver.find_element_by_link_text("Close").click()
        driver.find_element_by_link_text("Iterations").click()
        driver.find_element_by_link_text("New Iteration").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_title"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("SAMUEL ADDED THIS")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            "only Samuel can make iterations")
        driver.find_element_by_xpath(
            "//div[@id='id_start_date_popover']/div/span/i").click()
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//tr[1]/td[4]"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath("//tr[1]/td[4]").click()
        driver.find_element_by_xpath(
            "//div[@id='id_end_date_popover']/div/span/i").click()
        for i in range(60):
            try:
                if self.is_element_present(
                        By.XPATH, "//div[5]/div[3]/table/tbody/tr[2]/td[4]"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath(
            "//div[5]/div[3]/table/tbody/tr[2]/td[4]").click()
        driver.find_element_by_link_text("Create").click()
        time.sleep(1)
        driver.find_element_by_link_text("SamuelLJackson").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Return to Home").click()
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("george")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Open").click()
        time.sleep(1)
        driver.find_element_by_link_text("george").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Return to Home").click()
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("SamuelLJackson")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("snakes")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Open").click()
        for i in range(60):
            try:
                if self.is_element_present(By.LINK_TEXT, "george"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_link_text("george").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_user_role"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        Select(driver.find_element_by_id("id_user_role")).select_by_visible_text(
            "Developer")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        driver.find_element_by_link_text("george").click()
        for i in range(60):
            try:
                if self.is_element_present(By.LINK_TEXT, "Close"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_link_text("Close").click()
        driver.find_element_by_css_selector(
            "i.glyphicon.glyphicon-minus").click()
        for i in range(60):
            try:
                if self.is_element_present(By.LINK_TEXT, "Delete"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_link_text("Delete").click()
        time.sleep(1)
        driver.find_element_by_link_text("Close").click()
        time.sleep(1)
        driver.find_element_by_link_text("SamuelLJackson").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Return to Home").click()
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("george")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("1234")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("george").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Return to Home").click()
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("SamuelLJackson")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("snakes")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_link_text("Delete").click()
        for i in range(60):
            try:
                if self.is_element_present(By.LINK_TEXT, "Delete Project"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_link_text("Delete Project").click()
        time.sleep(1)
        driver.find_element_by_link_text("SamuelLJackson").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Return to Home").click()

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
