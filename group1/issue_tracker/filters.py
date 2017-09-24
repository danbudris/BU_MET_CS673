
import datetime

from issue_tracker import models
from django.db.models import Q
from django.utils import timezone


class FilterIssueQueryset(object):
    """Filtering the Issue model based on criteria provided.

    This takes the form data provided and filters the queryset down
    based on that form.  This class is tightly coupled with models.Issue
    object.
    """

    def __init__(self, data):
        self.__dict__.update(data)

    def filter_title(self, query):
        if self.title:
            query &= Q(title__icontains=self.title)
        return query

    def filter_description(self, query):
        if self.description:
            query &= Q(description__icontains=self.description)
        return query

    def filter_status(self, query):
        if self.status:
            query &= Q(status=self.status)
        return query

    def filter_issue_type(self, query):
        if self.issue_type:
            query &= Q(issue_type=self.issue_type)
        return query

    def filter_priority(self, query):
        if self.priority:
            query &= Q(priority=self.priority)
        return query

    def filter_project(self, query):
        if self.project:
            query &= Q(project=self.project)
        return query

    def convert_date_min(self, item):
        return timezone.make_aware(datetime.datetime.combine(
            item, datetime.time.min),
            timezone.get_current_timezone())

    def convert_date_max(self, item):
        return timezone.make_aware(datetime.datetime.combine(
            item, datetime.time.max),
            timezone.get_current_timezone())

    def filter_submitted_date(self, query):
        if self.submitted_date:
            query &= Q(submitted_date__range=(
                self.convert_date_min(self.submitted_date),
                self.convert_date_max(self.submitted_date)))
        return query

    def filter_modified_date(self, query):
        if self.modified_date:
            query &= Q(modified_date__range=(
                self.convert_date_min(self.modified_date),
                self.convert_date_max(self.modified_date)))
        return query

    def filter_closed_date(self, query):
        if self.closed_date:
            query &= Q(closed_date__range=(
                self.convert_date_min(self.closed_date),
                self.convert_date_max(self.closed_date)))
        return query

    def filter_assignee(self, query):
        if self.assignee:
            query &= Q(assignee=self.assignee)
        return query

    def filter_reporter(self, query):
        if self.reporter:
            query &= Q(reporter=self.reporter)
        return query

    def filter_verifier(self, query):
        if self.verifier:
            query &= Q(verifier=self.verifier)
        return query


def filter_issue_results(data):
    """Take an initial dataset and filter it down to the specific data needed.

    Args:
      data: The form.cleaned_data provided.
    Returns:
      A list of issues found.
    """
    query = Q()
    final_query = []
    filter_queryset = FilterIssueQueryset(data)

    # Based on the parameters from the form, find the appropriate filter
    # method and call it against the current queryset.
    for key in data.iterkeys():
        handler = getattr(filter_queryset, 'filter_%s' % key)
        if handler:
            query = handler(query)

    if query and len(query):
        final_query = models.Issue.objects.filter(query).select_related()
    return final_query
