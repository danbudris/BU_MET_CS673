from django.db import models
from django.contrib.auth.models import User
from project import Project

ROLE_CLIENT = "client"
ROLE_DEVELOPER = "developer"
ROLE_OWNER = "owner"

PERM_CREATE_STORY = "CreateStory"
PERM_EDIT_STORY = "EditStory"
PERM_DELETE_STORY = "DeleteStory"


class UserAssociation(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    role = models.CharField(max_length=128)

    def get_permission(self, permission):
        # Checks whether the association's user has the specified permission on the
        # association's project.
        return permission in self.get_role_permissions(self.role)

        def test_function():
            return false

    def get_role_permissions(self, role):

        # The role passed should be one of the string constants defined above.
        # This method is where the permissions associated with a role are defined.
        # It should return an array of strings representing permissions.
        role_dictionary = {
            # <<<<<<< HEAD
            #             ROLE_CLIENT: [PERM_CREATE_STORY],
            #             ROLE_DEVELOPER: [PERM_CREATE_STORY, PERM_EDIT_STORY, PERM_DELETE_STORY],
            #             ROLE_OWNER: [PERM_CREATE_STORY, PERM_EDIT_STORY, PERM_DELETE_STORY,
            #                           "AddUser", "DeleteUser", "ChangePermissions", "EditProject", "DeleteProject", "AddIteration"]
            # =======
            ROLE_CLIENT: [PERM_CREATE_STORY, PERM_EDIT_STORY, "AcceptStory"],
            ROLE_DEVELOPER: [PERM_CREATE_STORY, PERM_EDIT_STORY, "EditHours", "EditPoints",
                             "ChangeStoryStatus", "AddTasks", "EditTasks", "EditOwner"],
            ROLE_OWNER: [PERM_CREATE_STORY, PERM_EDIT_STORY, PERM_DELETE_STORY, "AcceptStory",
                         "EditHours", "EditPoints", "SelectStoryStatus", "AddTasks", "EditTasks",
                         "AddUser", "DeleteUser", "ChangePermissions",
                         "PauseStory", "EditAccepted", "EditPaused", "MoveStoryToIteration",
                         "EditProject", "DeleteProject", "AddIteration", "EditIteration", "DeleteIteration", "EditOwner"]
            # >>>>>>> newfeature-addpermissionforeditstory
        }
        # TODO: exception handling if permission string not found.
        return role_dictionary[role]

    class Meta:
        app_label = 'requirements'
