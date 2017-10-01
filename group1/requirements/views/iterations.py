from django import forms
from requirements import models
from requirements.views import projects
from requirements.models import project_api
from requirements.models import user_manager
from requirements.models import story as mdl_story
from requirements.models import iteration as mdl_iteration
from requirements.models.user_manager import user_owns_project
from requirements.models.user_association import UserAssociation
from forms import IterationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import datetime


PERMISSION_OWN_PROJECT = 'requirements.own_project'


@login_required(login_url='/signin')
def iteration(request, projectID, iterationID):
    if project_api.can_user_access_project(request.user.id, projectID):
        projects = project_api.get_projects_for_user(request.user.id)
        project = project_api.get_project(projectID)
        if project is None:
            return redirect('/req/projects')
        association = UserAssociation.objects.get(
            user=request.user,
            project=project)
        iterations = project_api.get_iterations_for_project(project)
        iteration = project_api.get_iteration(iterationID)
        if iteration is not None:
            stories = project_api.get_stories_for_iteration(iteration)
        else:
            stories = project_api.get_stories_with_no_iteration(project)
        context = {'projects': projects,
                   'project': project,
                   'association': association,
                   'iterations': iterations,
                   'iteration': iteration,
                   'stories': stories,
                   'owns_project': project_api.user_owns_project(request.user, project)
                   }
        if iteration is None:
            context['isIceBox'] = True
        return render(request, 'IterationDetail.html', context)
    else:
        # return HttpResponse("You cannot access project " + proj)
        return redirect('/req/projects')


@login_required(login_url='/signin')
@user_owns_project()
def new_iteration(request, projectID):
    project = project_api.get_project(projectID)
    if request.method == 'POST':
        form = IterationForm(request.POST)
        if form.is_valid():
            mdl_iteration.create_iteration(project, request.POST)
            form.save(commit=False)
            # return redirect('/req/projectdetail/' + projectID)
            # return empty string and do the redirect stuff in front-end
            return HttpResponse('')
    else:
        form = IterationForm()
    context = {
        'title': 'Create New Iteration',
        'action': '/req/newiteration/' + projectID,
        'form': form,
        'button_desc': 'Create',
    }
    return render(request, 'IterationSummary.html', context)


@login_required(login_url='/signin')
@user_owns_project()
def edit_iteration(request, projectID, iterationID):
    project = project_api.get_project(projectID)
    iteration = mdl_iteration.get_iteration(iterationID)
    if project is None or iteration is None or iteration.project != project:
        # return redirect('/req/projectdetail/' + projectID)
        # return empty string and do the redirect stuff in front-end
        return HttpResponse('')
    if request.method == "POST":
        form = IterationForm(request.POST, instance=iteration)
        if form.is_valid():
            form.save(commit=True)
            # return redirect('/req/projectdetail/' + projectID)
            # return empty string and do the redirect stuff in front-end
            return HttpResponse('')
    else:
        form = IterationForm(instance=iteration)
    context = {
        'title': 'Edit Iteration',
        'action': '/req/edititeration/' + projectID + '/' + iterationID,
        'form': form,
        'button_desc': 'Save Changes'
    }
    return render(request, 'IterationSummary.html', context)


@login_required(login_url='/signin')
@user_owns_project()
def delete_iteration(request, projectID, iterationID):
    project = project_api.get_project(projectID)
    iteration = mdl_iteration.get_iteration(iterationID)
    if project is None or iteration is None or iteration.project != project:
        # return redirect('/req/projectdetail/' + projectID)
        # return empty string and do the redirect stuff in front-end
        return HttpResponse('')
    if request.method == "POST":
        iteration.delete()
        # return redirect('/req/projectdetail/' + projectID)
        # return empty string and do the redirect stuff in front-end
        return HttpResponse('')
    else:
        form = IterationForm(instance=iteration)
    context = {
        'title': 'Edit Iteration',
        'confirm_message': 'This is an irreversible procedure ! You will lose all information about this iteration and stories it contains !',
        'action': '/req/deleteiteration/' + projectID + '/' + iterationID,
        'form': form,
        'button_desc': 'Delete'
    }
    return render(request, 'IterationSummary.html', context)


@login_required(login_url='/signin')
def list_iterations_for_project(request, projectID):
    project = project_api.get_project(projectID)
    iterations = mdl_iteration.get_iterations_for_project(project)
    context = {
        'project': project,
        'iterations': iterations,
        'owns_project': project_api.user_owns_project(request.user, project),
    }
    return render(request, 'SideBarIters.html', context)


@login_required(login_url='/signin')
def list_iterations_for_project_with_selection(
        request, projectID, iterationID):
    project = project_api.get_project(projectID)
    iterations = mdl_iteration.get_iterations_for_project(project)
    iteration = mdl_iteration.get_iteration(iterationID)
    context = {
        'project': project,
        'iterations': iterations,
        'iteration': iteration,
        'owns_project': project_api.user_owns_project(request.user, project),
    }
    if iteration is None:
        context['isIceBox'] = True
    return render(request, 'SideBarIters.html', context)
