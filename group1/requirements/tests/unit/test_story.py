from django.test import TestCase
from django.contrib.auth.models import User
from requirements import models
from requirements.models import project
from requirements.models import project_api
from requirements.models import user_association
from requirements.models import user_manager
from requirements.models import story
from requirements.models.project import Project
from requirements.models.user_association import UserAssociation
from requirements.models.iteration import Iteration
from requirements.models.story import Story
import datetime
from cgi import FieldStorage
from django.db import transaction


class Obj():
    pass


class ProjectTestCase(TestCase):

    def setUp(self):
        self.__clear()

        self.__project = Project(title="title", description="desc")
        self.__project.save()
        self.__user = User(username="testUser", password="pass")
        self.__user.save()

    def tearDown(self):
        self.__clear()

    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete

    def test_get_project_stories(self):
        p = Project(title="title", description="desc")
        p.save()
        iterations = models.project_api.get_iterations_for_project(p)
        stories = models.story.get_stories_for_project(p)
        self.assertEqual(False, stories.exists())

    def test_get_project_stories_one(self):
        p = Project(title="title", description="desc")
        p.save()
        models.story.create_story(p, {"title": "title",
                                      "description": "desc",
                                      "reason": "reason",
                                      "test": "test",
                                      "status": 1})

        iterations = models.project_api.get_iterations_for_project(p)
        stories = models.story.get_stories_for_project(p)
        self.assertEqual(True, stories.exists())

    def test_create_story_pass(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())

    def test_create_story_fail(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}

        # pass a null project
        s = models.story.create_story(None, fields)
        self.assertEqual(0, self.__project.story_set.count())

        # create a project, but don't save it
        p = Project(title="title", description="description")
        try:
            with transaction.atomic():
                s = models.story.create_story(p, fields)
        except Exception:
            pass
        self.assertEqual(0, self.__project.story_set.count())

    def test_delete_story_pass(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        models.story.delete_story(s.id)
        self.assertEqual(0, self.__project.story_set.count())

    def test_delete_story_fail(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        models.story.delete_story(s.id - 1)
        self.assertEqual(1, self.__project.story_set.count())
