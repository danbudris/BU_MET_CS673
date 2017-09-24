from django.db import models
from project import Project

# A file attached to a project


class ProjectFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='project_files')
    project = models.ForeignKey(Project)
