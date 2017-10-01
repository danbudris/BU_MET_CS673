from django.db import models
from base import ProjMgmtBase
from project import Project

import datetime


class Iteration(ProjMgmtBase):

    start_date = models.DateField()
    end_date = models.DateField()
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'requirements'


def create_iteration(project, fields):
    if project is None:
        return None
    if fields is None:
        return None

    title = fields.get('title', '')
    description = fields.get('description', '')

    str_start_date = fields.get('start_date', '')
    if str_start_date == '':
        str_start_date = datetime.today().strftime("%m/%d/%Y")
    start_date = datetime.datetime.strptime(str_start_date, "%m/%d/%Y").date()

    str_end_date = fields.get('end_date', '')
    if str_end_date == '':
        str_end_date = datetime.today().strftime("%m/%d/%Y")
    end_date = datetime.datetime.strptime(str_end_date, "%m/%d/%Y").date()

    iteration = Iteration(title=title, description=description,
                          start_date=start_date, end_date=end_date, project=project)
    iteration.save()
    return iteration


def get_iteration(iterationID):
    try:
        return Iteration.objects.get(id=iterationID)
    except Exception as e:
        return None


def get_iterations_for_project(project):
    if project is None:
        return None
    return Iteration.objects.filter(project__id=project.id)


def move_story_to_iteration(story, iteration):
    if story is None or iteration is None or story.project != iteration.project:
        return None
    story.iteration = iteration
    story.save()


def move_story_to_icebox(story):
    if story is None:
        return None
    story.iteration = None
    story.save()
