from django.test import TestCase
from django.contrib.auth.models import User
from requirements.models import user_manager
from requirements.models.user_association import UserAssociation
from requirements.models import user_association
from requirements.models.project import Project


class RoleTestCase(TestCase):

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

    def __addUserAsClient(self):
        ua = UserAssociation(
            project=self.__project,
            user=self.__user,
            role=user_association.ROLE_CLIENT)
        ua.save()

    def __addUserAsDev(self):
        ua = UserAssociation(
            project=self.__project,
            user=self.__user,
            role=user_association.ROLE_DEVELOPER)
        ua.save()

    def __addUserAsOwner(self):
        ua = UserAssociation(
            project=self.__project,
            user=self.__user,
            role=user_association.ROLE_OWNER)
        ua.save()

    def testAddStoryAsClient(self):
        self.__addUserAsClient()
        self.assertEquals(
            user_manager.canCreateStoryInProject(
                userID=self.__user.id,
                projectID=self.__project.id),
            True)

    def testAddStoryAsDev(self):
        self.__addUserAsDev()
        self.assertEquals(
            user_manager.canCreateStoryInProject(
                userID=self.__user.id,
                projectID=self.__project.id),
            True)

    def testAddStoryAsOwner(self):
        self.__addUserAsOwner()
        self.assertEquals(
            user_manager.canCreateStoryInProject(
                userID=self.__user.id,
                projectID=self.__project.id),
            True)

    def testAddStoryNoAssoc(self):
        self.assertEquals(
            user_manager.canCreateStoryInProject(
                userID=self.__user.id,
                projectID=self.__project.id),
            False)

    def testEditStoryNoAssoc(self):
        self.assertEquals(
            user_manager.canEditStoryInProject(
                userID=self.__user.id,
                projectID=self.__project.id),
            False)

    def testEditStoryAsClient(self):
        self.__addUserAsClient()
        self.assertEquals(
            user_manager.canEditStoryInProject(
                userID=self.__user.id,
                projectID=self.__project.id),
            True)

    def testEditStoryAsDev(self):
        self.__addUserAsDev()
        self.assertEquals(
            user_manager.canEditStoryInProject(
                userID=self.__user.id,
                projectID=self.__project.id),
            True)

    def testEditStoryAsOwner(self):
        self.__addUserAsOwner()
        self.assertEquals(
            user_manager.canEditStoryInProject(
                userID=self.__user.id,
                projectID=self.__project.id),
            True)

    def testIsOwner_NoAssoc(self):
        self.assertEquals(
            user_manager.isOwner(
                userID=self.__user.id,
                projectID=self.__project.id),
            False)

    def testIsOwner_IsOwner(self):
        self.__addUserAsOwner()
        self.assertEquals(
            user_manager.isOwner(
                userID=self.__user.id,
                projectID=self.__project.id),
            True)

    def testIsOwner_IsOwner(self):
        self.__addUserAsDev()
        self.assertEquals(
            user_manager.isOwner(
                userID=self.__user.id,
                projectID=self.__project.id),
            False)
