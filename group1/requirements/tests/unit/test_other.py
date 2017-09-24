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


class Obj():
    pass


class ProjectTestCase(TestCase):

    def setUp(self):
        self.__clear()

        self.__user = User(username="testUser", password="pass")
        self.__user.save()

    def tearDown(self):
        self.__clear()

    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete

    def test_add_story_to_iteration(self):
        p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"
        start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(
            title,
            description,
            start_date,
            end_date,
            p.id)

        story = models.story.create_story(p, {'title': "title",
                                              'description': "description",
                                              'test': "",
                                              'reason': "reason",
                                              'status': 1})

        models.project_api.add_story_to_iteration(story, iteration)
        self.assertEqual(iteration, story.iteration)

    def test_add_story_to_iteration_story_not_in_project(self):
        p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"
        start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(
            title,
            description,
            start_date,
            end_date,
            p.id)

        p2 = Project(title="title2", description="desc2")
        p2.save()

        story = models.story.create_story(p2, {'title': "title",
                                               'description': "description",
                                               'test': '',
                                               'reason': '',
                                               'status': 1})
        try:
            models.project_api.add_story_to_iteration(story, iteration)
            self.fail(
                "Adding a story to an invalid iteration did not throw an exception")
        except(ValueError):
            pass

    def test_get_project_stories_for_iteration(self):
        p = Project(title="title", description="desc")
        p.save()
        iteration = models.project_api.add_iteration_to_project(
            "title",
            "description",
            datetime.date.today(),
            datetime.date.max,
            p.id)
        story = models.story.create_story(p, {'title': "title",
                                              'description': "description",
                                              'test': "",
                                              'reason': "",
                                              'status': 1})
        models.project_api.add_story_to_iteration(story, iteration)
        stories = models.project_api.get_stories_for_iteration(iteration)

        self.assertEquals(stories.count(), 1)
        self.assertEquals(stories[0], story)

    def test_get_project_stories_with_no_iteration(self):
        p = Project(title="title", description="desc")
        p.save()
        iteration = models.project_api.add_iteration_to_project(
            "title",
            "description",
            datetime.date.today(),
            datetime.date.max,
            p.id)
        story = models.story.create_story(p, {'title': "title",
                                              'description': "description",
                                              'test': "",
                                              'reason': "",
                                              'status': 1})
        stories = models.project_api.get_stories_with_no_iteration(p)

        self.assertEquals(stories.count(), 1)
        self.assertEquals(stories[0], story)

    def test_user_owns_project_true(self):
        owner = User(
            username="user",
            password="password",
            email="email@address.com")
        owner.save()

        project = models.project_api.create_project(
            owner, {
                'title': 'title', 'description': 'description'})
        self.assertEquals(
            models.project_api.user_owns_project(
                owner,
                project),
            True)

    def test_user_owns_project_false(self):
        owner = User(
            username="user",
            password="password",
            email="email@address.com")
        owner.save()

        user = User(
            username="user2",
            password="password",
            email="email@address.com")
        user.save()

        project = models.project_api.create_project(
            owner, {
                'title': 'title', 'description': 'description'})
        self.assertEquals(
            models.project_api.user_owns_project(
                user,
                project),
            False)
