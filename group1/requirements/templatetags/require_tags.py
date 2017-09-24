# This file contains custom tags required for templates in RequireTracker.

from django import template

register = template.Library()


def check_permission(association, the_project, permission):
    # Boolean. Checks two things:
    # 1) Is the association matched to the specified project?
    # 2) Does the user have the specified permission for that project?
    # Returns true if both are true, otherwise false.

    if association.project == the_project and association.get_permission(
            permission):
        return True
    else:
        return False


register.assignment_tag(check_permission)
