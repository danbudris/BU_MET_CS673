from django import forms
from requirements import models
from requirements.models.story import Story
from requirements.models.project import Project
from requirements.models import project_api
from forms import AddCommentForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render, redirect


def new_comment(request, storyID, projectID):
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            project = project_api.get_project(projectID)
            story = story.get_story(storyID)
            story_comment = models.story_comment.create_story_comment(
                request.user,
                story,
                request.POST)
            story_comment = form.save(commit=False)
            return redirect('/project/' + projectID)
    else:
        form = AddCommentForm()

    context = {'title': 'New Story Comment',
               'form': form,
               'action': '/newcomment/' + storyID,
               'desc': 'Create Story Comment'}
    return render(request, 'CommentForm.html', context)
