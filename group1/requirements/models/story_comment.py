from django.db import models
from django.contrib.auth.models import User
from story import Story
import datetime


class StoryComment(models.Model):
    story = models.ForeignKey(Story)
    title = models.CharField(default='', max_length=1024)
    comment = models.CharField(default='', max_length=1024)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'requirements'


def get_comments_for_story(story):
    if story is None:
        return None
    return StoryComment.objects.filter(story_id=story.id)


def get_comment(commentID):
    try:
        return StoryComment.objects.get(id=commentID)
    except Exception as e:
        return None


def create_comment(story, fields):
    if story is None:
        return None
    if fields is None:
        return None

    title = fields.get('title', '')
    comment = fields.get('comment', '')

    aComment = StoryComment(
        story=story,
        title=title,
        comment=comment,
    )
    aComment.save()
    return aComment
