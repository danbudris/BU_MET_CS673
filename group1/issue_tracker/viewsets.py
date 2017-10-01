from django.contrib.auth import models as auth_models
from rest_framework import viewsets
from issue_tracker import models as it_models
from issue_tracker import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = auth_models.User.objects.all()
    serializer_class = serializers.UserSerializer


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = it_models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer
