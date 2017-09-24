from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from requirements.models import Project, Story, Task, Iteration
from django.contrib.auth.models import User
import unittest
import time
import re
import datetime


class TestStory(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        datetime.datetime.strptime("04/01/2015", "%m/%d/%Y").date()
        self.user = User(
            username='admin',
            password='pass'
        )
        self.project = Project(
            title='___Test Project 1___',
            description='___Test Project 1 Description__'
        )
        self.iteration = Iteration(
            title='___Test Iteration 1___',
            description='___Test Iteration 1 Description___',
            start_date=datetime.datetime.strptime(
                "04/01/2015",
                "%m/%d/%Y").date(),
            end_date=datetime.datetime.strptime(
                "04/30/2015",
                "%m/%d/%Y").date()
        )
        self.story = Story(
            title='___Test Story 1___',
            description='___Test Story 1 Description',
            reason='___Story Reason___',
            test='___Story Test___',
            hours=3,
            status='Started',
            points='3 Points'
        )
        self.story_edit = Story(
            title='___Test Story 1 (Edit)___',
            description='___Test Story 1 Description (Edit)___',
            reason='___Story Reason (Edit)___',
            test='___Story Test (Edit)___',
            hours=5,
            status='Completed',
            points='5 Points',
        )
        self.tasks = (Task(description='___Task Test 1___'),
                      Task(description='___Task Test 2___'),
                      Task(description='___Task Test 3___'))
        self.tasks_edit = (Task(description='___Task Test 1 (Edit)___'),
                           Task(description='___Task Test 2 (Edit)___'),
                           Task(description='___Task Test 3 (Edit)___'))

    def test_story(self):
        if not self.home():
            self.assertTrue(False, "Error navigating to home page.")
        if not self.login():
            self.assertTrue(False, "Error logging in.")
        if not self.create_project():
            self.assertTrue(False, "Error creating new project.")
        if not self.create_iteration():
            self.assertTrue(False, "Error creating new iteration.")
        if not self.create_story():
            self.assertTrue(False, "Error creating new user story.")
        if not self.move_story():
            self.assertTrue(False, "Error moving user story.")
        if not self.edit_story():
            self.assertTrue(False, "Error editing user story.")
        if not self.delete_story():
            self.assertTrue(False, "Error deleting user story.")
        if not self.delete_project():
            self.assertTrue(False, "Error deleting project.")
        if not self.logout():
            self.assertTrue(False, "Error logging out.")

    def home(self):
        try:
            self.driver.get(self.base_url + "/")

        except Exception:
            return False
        return True

    def login(self):
        try:
            driver = self.driver
            user = self.user
            driver.find_element_by_link_text("Sign In").click()
            driver.find_element_by_id("username").clear()
            driver.find_element_by_id("username").send_keys(user.username)
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("password").send_keys(user.password)
            driver.find_element_by_xpath("//button[@type='submit']").click()

        except Exception:
            return False
        return True

    def create_project(self):
        try:
            driver = self.driver
            project = self.project
            driver.find_element_by_css_selector(
                "i.glyphicon.glyphicon-plus").click()
            time.sleep(2)
            driver.find_element_by_id("id_title").clear()
            driver.find_element_by_id("id_title").send_keys(project.title)
            driver.find_element_by_id("id_description").clear()
            driver.find_element_by_id(
                "id_description").send_keys(project.description)
            driver.find_element_by_link_text("Create Project").click()
            time.sleep(2)

        except Exception:
            return False
        return True

    def create_iteration(self):
        driver = self.driver
        iter = self.iteration
        try:
            driver.find_element_by_xpath(
                "//a[contains(@data-proj-sidebar, '" + self.project.title + "')]").click()
            time.sleep(2)
            driver.find_element_by_xpath(
                "//a[contains(@data-load-iter, '" + self.project.title + "')]").click()
            time.sleep(2)
            driver.find_element_by_xpath(
                "//a[contains(@data-new-iter, '" + self.project.title + "')]").click()
            time.sleep(2)
            driver.find_element_by_id("id_title").clear()
            driver.find_element_by_id("id_title").send_keys(iter.title)
            driver.find_element_by_id("id_description").clear()
            driver.find_element_by_id(
                "id_description").send_keys(iter.description)
            driver.find_element_by_xpath(
                "//div[@id='id_start_date_popover']/div/span/i").click()
            time.sleep(1)
            driver.find_element_by_xpath("//tr[1]/td[4]").click()
            time.sleep(1)
            driver.find_element_by_xpath(
                "//div[@id='id_end_date_popover']/div/span/i").click()
            time.sleep(1)
            driver.find_element_by_xpath(
                "//div[5]/div[3]/table/tbody/tr[2]/td[5]").click()
            time.sleep(1)
            driver.find_element_by_link_text("Create").click()
            time.sleep(2)

        except Exception:
            return False
        return True

    def delete_project(self):
        try:
            driver = self.driver
            project = self.project
            driver.find_element_by_link_text("Dashboard").click()
            driver.find_element_by_xpath(
                "//a[contains(@data-del-proj, '" + project.title + "')]").click()
            driver.find_element_by_link_text("Delete Project").click()
            time.sleep(2)

        except Exception:
            return False
        return True

    def create_story(self):
        try:
            driver = self.driver
            driver.find_element_by_xpath(
                "//a[contains(@data-open-proj, '" + self.project.title + "')]").click()
            driver.find_element_by_css_selector(
                "i.glyphicon.glyphicon-plus").click()
            self.enter_story_data(self.story, self.tasks, True)
            driver.find_element_by_link_text("Create User Story").click()
            time.sleep(2)
            retval = self.is_element_present(
                By.XPATH,
                "//a[contains(@data-story, '" + self.story.title + "')]")

        except Exception:
            return False
        return retval

    def edit_story(self):
        try:
            driver = self.driver
            driver.find_element_by_xpath(
                "//a[contains(@data-edit-story, '" + self.story.title + "')]").click()
            self.enter_story_data(self.story_edit, self.tasks_edit, False)
            driver.find_element_by_link_text("Save Changes").click()
            time.sleep(2)
            retval = self.is_element_present(
                By.XPATH,
                "//a[contains(@data-story, '" + self.story_edit.title + "')]")

        except Exception:
            return False
        return retval

    def move_story(self):
        driver = self.driver
        story = self.story
        iter = self.iteration
        driver.find_element_by_xpath(
            "//button[contains(@data-move-story, '" + story.title + "')]").click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "//a[contains(text(),'" + iter.title + "')]").click()
        time.sleep(1)

        return True

    def delete_story(self):
        try:
            driver = self.driver
            driver.find_element_by_xpath(
                "//a[contains(@data-del-story, '" + self.story_edit.title + "')]").click()
            driver.find_element_by_link_text("Delete User Story").click()
            time.sleep(2)
            driver.implicitly_wait(2)
            retval = not self.is_element_present(
                By.XPATH,
                "//a[contains(@data-story, '" + self.story_edit.title + "')]")
            driver.implicitly_wait(30)

        except Exception:
            return False
        return retval

    def enter_story_data(self, story, tasks, isNew):
        try:
            driver = self.driver
            user = self.user
            driver.find_element_by_xpath("//input[@id='id_title']").clear()
            driver.find_element_by_xpath(
                "//input[@id='id_title']").send_keys(story.title)
            driver.find_element_by_xpath(
                "//textarea[@id='id_description']").clear()
            driver.find_element_by_xpath(
                "//textarea[@id='id_description']").send_keys(story.description)
            driver.find_element_by_id("id_reason").clear()
            driver.find_element_by_id("id_reason").send_keys(story.reason)
            driver.find_element_by_id("id_test").clear()
            driver.find_element_by_id("id_test").send_keys(story.test)

            if isNew:
                driver.find_element_by_id("id_task_set-0-description").clear()
                driver.find_element_by_id(
                    "id_task_set-0-description").send_keys(tasks[0].description)
                driver.find_element_by_link_text("New Task").click()
                time.sleep(1)
                driver.find_element_by_id("id_task_set-1-description").clear()
                driver.find_element_by_id(
                    "id_task_set-1-description").send_keys(tasks[1].description)
                driver.find_element_by_link_text("New Task").click()
                time.sleep(1)
                driver.find_element_by_id("id_task_set-2-description").clear()
                driver.find_element_by_id(
                    "id_task_set-2-description").send_keys(tasks[2].description)
            else:
                driver.find_element_by_id("id_task_set-0-description").clear()
                driver.find_element_by_id(
                    "id_task_set-0-description").send_keys(tasks[0].description)
                driver.find_element_by_id("id_task_set-1-description").clear()
                driver.find_element_by_id(
                    "id_task_set-1-description").send_keys(tasks[1].description)
                driver.find_element_by_id("id_task_set-2-description").clear()
                driver.find_element_by_id(
                    "id_task_set-2-description").send_keys(tasks[2].description)
            Select(
                driver.find_element_by_id("id_owner")).select_by_visible_text(
                user.username)
            driver.find_element_by_id("id_hours").clear()
            driver.find_element_by_id("id_hours").send_keys(story.hours)
            Select(
                driver.find_element_by_id("id_status")).select_by_visible_text(
                story.status)
            Select(
                driver.find_element_by_id("id_points")).select_by_visible_text(
                story.points)

        except Exception:
            return False
        return True

    def logout(self):
        try:
            driver = self.driver
            driver.find_element_by_link_text("admin").click()
            driver.find_element_by_link_text("Logout").click()
            driver.find_element_by_link_text("Home").click()

        except Exception:
            return False
        return True

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
