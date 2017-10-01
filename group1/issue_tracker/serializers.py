from django.contrib.auth import models as auth_models
from issue_tracker import models as it_models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ('url', 'username', 'email', 'groups')


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = it_models.Issue
        fields = (
            'pk',
            'title',
            'description',
            'status',
            'priority',
            'issue_type',
            'project',
            'reporter',
            'assignee',
            'submitted_date',
            'modified_date',
            'closed_date'
            )
