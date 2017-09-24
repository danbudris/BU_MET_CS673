from django.db import models
from story import Story


class Task(models.Model):
    story = models.ForeignKey(Story)
    description = models.CharField(max_length=1024, default='')
    # hours = models.IntegerField(default=0)
    # is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    class Meta:
        app_label = 'requirements'


def get_task(taskID):
    try:
        return Task.objects.get(id=taskID)
    except Exception as e:
        return None


def get_tasks_for_story(story):
    if story is None:
        return None
    return Task.objects.filter(story__id=story.id)


def create_task(story, fields):
    if story is None or fields is None:
        return None

    description = fields.get('description', '')
    if description == '':
        return

    task = Task(story=story, description=description)
    task.save()
    return task
