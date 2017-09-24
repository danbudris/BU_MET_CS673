from django.contrib.auth import models as auth_models
from django.core.urlresolvers import reverse
from django.db import models
from requirements.models import project as project_model

OPEN_STATUSES = (
    ('Open-New', 'New',),
    ('Open-Assigned', 'Assigned',),
    ('Open-Accepted', 'Accepted',),
    )

CLOSED_STATUSES = (
    ('Closed-Fixed', 'Fixed',),
    ('Closed-Verified', 'Verified',),
    ('Closed-Working as Intended', 'Working as Intended',),
    ('Closed-Obsolete', 'Obsolete',),
    ('Closed-Duplicate', 'Duplicate',),
    )

STATUSES = (OPEN_STATUSES + CLOSED_STATUSES)

TYPES = (
    ('Bug', 'Bug',),
    ('Feature', 'Feature Request',),
    ('Internal Cleanup', 'Internal Cleanup',),
    )

PRIORITIES = (
    ('High', 'High',),
    ('Medium', 'Medium',),
    ('Low', 'Low',),
    )


class Issue(models.Model):
    """Issue"""
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    issue_type = models.CharField(max_length=20, choices=TYPES)
    status = models.CharField(max_length=20, default='new', choices=STATUSES)
    priority = models.CharField(max_length=20, choices=PRIORITIES)

    # Project
    project = models.ForeignKey(project_model.Project,
                                null=True)
    # Dates
    submitted_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)
    closed_date = models.DateTimeField(null=True, editable=False)

    # Users
    reporter = models.ForeignKey(auth_models.User, related_name='reporter',
                                 null=True)
    assignee = models.ForeignKey(auth_models.User, related_name='assignee',
                                 blank=True, null=True)
    verifier = models.ForeignKey(auth_models.User, related_name='verifier',
                                 blank=True, null=True)

    class Meta(object):
        ordering = ['id']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_issue', kwargs={'pk': self.pk})


class IssueComment(models.Model):
    comment = models.TextField(max_length=2000)
    issue_id = models.ForeignKey(Issue, related_name='comments',
                                 blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    poster = models.ForeignKey(auth_models.User,
                               related_name='comments', blank=True,
                               null=True)
    is_comment = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('view_issue', kwargs={'pk': self.issue_id})
