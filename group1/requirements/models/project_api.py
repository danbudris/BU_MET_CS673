from user_association import UserAssociation
from project import Project
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from iteration import Iteration
from story import Story
import user_association


def get_all_projects():
    return Project.objects.all()


def get_associations_for_user(userID):
    # Returns the associations between this user and his/her projects,
    # including the user's role on those projects.
    return UserAssociation.objects.filter(user__id=userID)


def get_projects_for_user(userID):
    return Project.objects.filter(users__id__contains=userID)


def get_project(projectID):
    try:
        return Project.objects.get(id=projectID)
    except Exception as e:
        return None


def get_project_users(projectID):
    return UserAssociation.objects.filter(project__id=projectID)


def can_user_access_project(userID, projectID):
    return UserAssociation.objects.filter(
        user__id=userID, project__id=projectID).count() > 0


def create_project(user, fields):
    if user is None:
        return None
    if fields is None:
        return None
    try:
        u = User.objects.get(id=user.id)
    except ObjectDoesNotExist:
        return None

    title = fields.get('title', '')
    description = fields.get('description', '')
    proj = Project(title=title, description=description)
    proj.save()
    association = UserAssociation(
        user=user,
        project=proj,
        role=user_association.ROLE_OWNER)
    association.save()
    return proj


def add_user_to_project(projectID, username, user_role):
    try:
        proj = Project.objects.get(id=projectID)
        user = User.objects.get(username=username)
        association = UserAssociation(user=user, project=proj, role=user_role)
        association.save()

    except ObjectDoesNotExist:
        return


def remove_user_from_project(projectID, username):
    if projectID is None:
        return
    if username is None:
        return

    try:
        proj = Project.objects.get(id=projectID)
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return

    ua = UserAssociation.objects.get(project=proj, user=user)
    ua.delete()


def delete_project(project):
    if project is None:
        return None
    association = UserAssociation.objects.filter(project=project)
    association.delete()
    project.delete()


def add_iteration_to_project(
        title, description, start_date, end_date, projectID):
    if start_date is None:
        return None
    if end_date is None:
        return None
    if projectID is None:
        return None

    try:
        project = Project.objects.get(id=projectID)
    except ObjectDoesNotExist:
        return None

    iteration = Iteration(title=title,
                          description=description,
                          start_date=start_date,
                          end_date=end_date,
                          project=project)
    iteration.save()
    return iteration


def add_story_to_iteration(story, iteration):
    if story.project != iteration.project:
        raise ValueError("The story and iteration are not in the same project")
    story.iteration = iteration
    story.save()


def move_story_to_icebox(story):
    story.iteration = None
    story.save()


def get_iterations_for_project(project):
    return Iteration.objects.filter(project__id=project.id)


def user_owns_project(user, project):
    ua_list = UserAssociation.objects.filter(user=user, project=project)
    if not ua_list.exists():
        return False
    return user_association.ROLE_OWNER == ua_list[0].role


def change_user_role(the_project, the_user, the_role):
    # Finds the user's association in the specified project, and changes role to the
    # specified role.
    try:
        association = UserAssociation.objects.get(
            user=the_user,
            project=the_project)
        association.role = the_role
        # print "Supposedly ran the code that changed "+(the_user.username)+"'s role to "+the_role+"."
        # print "Association.role is "+association.role+"."
        association.save()
    except UserAssociation.DoesNotExist:
        print "Error. Could not find association where user = " + (the_user.username) + " and project = " + the_project + "."

    return


def get_stories_for_iteration(iteration):
    return Story.objects.filter(iteration=iteration)


def get_stories_with_no_iteration(project):
    return Story.objects.filter(project=project, iteration=None)


def get_iteration(iterationID):
    try:
        return Iteration.objects.get(id=iterationID)
    except Exception as e:
        return None
