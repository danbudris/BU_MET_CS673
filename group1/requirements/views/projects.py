from django import forms
from requirements import models
from requirements.models import project_api
from requirements.models import user_manager, user_association
from requirements.models import story as mdl_story
from requirements.models import iteration as mdl_iteration
from requirements.models.user_association import UserAssociation
from django.http import HttpResponse, HttpResponseRedirect
from forms import IterationForm
from forms import ProjectForm
from forms import SelectAccessLevelForm
from forms import FileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render, redirect
import datetime
from requirements.models.user_manager import user_owns_project
from requirements.models.user_manager import user_can_access_project
from requirements.models.files import ProjectFile
from django.utils.encoding import smart_str
PERMISSION_OWN_PROJECT = 'requirements.own_project'


@login_required(login_url='/signin')
def list_projects(request):
    # Loads the DashBoard template, which contains a list of the project the user is
    # associated with, and an option to create new projects if one has that
    # permission.
    context = {
        'canOwnProject': request.user.has_perm(PERMISSION_OWN_PROJECT),
        'projects': project_api.get_projects_for_user(request.user.id),
        'theUser': request.user,
        'associationsWithUser': project_api.get_associations_for_user(request.user.id)
    }
    # if request.user.is_authenticated():
    #     logedInUser = request.user
    #     logedInUser.set_unusable_password()
    #     context['user'] = logedInUser
    return render(request, 'DashBoard.html', context)


@login_required(login_url='/signin')
def project(request, projectID):
    project = project_api.get_project(projectID)
    if project is None:
        return redirect('/req/projects')

    iterations = mdl_iteration.get_iterations_for_project(project)
    association = UserAssociation.objects.get(
        user=request.user,
        project=project)

    context = {'projects': project_api.get_projects_for_user(request.user.id),
               'project': project,
               'stories': mdl_story.get_stories_for_project(project),
               'iterations': iterations,
               'association': association,
               'canOwnProject': request.user.has_perm(PERMISSION_OWN_PROJECT),
               }
    return render(request, 'ProjectDetail.html', context)


@login_required(login_url='/signin')
@permission_required(PERMISSION_OWN_PROJECT)
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_api.create_project(request.user, request.POST)
            project = form.save(commit=False)
            # return redirect('/req/projects')
            # return empty string and do the redirect stuff in front-end
            return HttpResponse('')
    else:
        form = ProjectForm()

    context = {'projects': project_api.get_projects_for_user(request.user.id),
               'canOwnProject': request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title': 'New Project',
               'form': form, 'action': '/req/newproject', 'button_desc': 'Create Project'}
    return render(request, 'ProjectSummary.html', context)


@login_required(login_url='/signin')
@user_owns_project()
def edit_project(request, projectID):
    project = project_api.get_project(projectID)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=True)
            # return redirect('/req/projects')
            # return empty string and do the redirect stuff in front-end
            return HttpResponse('')
    else:
        form = ProjectForm(instance=project)

    context = {'projects': project_api.get_projects_for_user(request.user.id),
               'canOwnProject': request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title': 'Edit Project',
               'form': form, 'action': '/req/editproject/' + projectID, 'button_desc': 'Save Changes'}
    return render(request, 'ProjectSummary.html', context)


@login_required(login_url='/signin')
@user_owns_project()
def delete_project(request, projectID):
    project = project_api.get_project(projectID)
    if project is None:
        # return redirect('/req/projects')
        # return empty string and do the redirect stuff in front-end
        return HttpResponse('')
    if request.method == 'POST':
        project_api.delete_project(project)
        # return redirect('/req/projects')
        # return empty string and do the redirect stuff in front-end
        return HttpResponse('')
    else:
        form = ProjectForm(instance=project)

    context = {'projects': project_api.get_projects_for_user(request.user.id),
               'canOwnProject': request.user.has_perm(PERMISSION_OWN_PROJECT),
               'title': 'Delete Project',
               'confirm_message': 'This is an unrevert procedure ! You will lose all information about this project !',
               'form': form, 'action': '/req/deleteproject/' + projectID, 'button_desc': 'Delete Project'}
    return render(request, 'ProjectSummary.html', context)

#=========================================================================
# @login_required(login_url='/accounts/login/')
# @permission_required('projects.own_project')
# def createProject(request):
#     proj = models.createProject(request.user, request.POST)
#     return redirect('/projects')
#=========================================================================


@login_required(login_url='/signin')
def list_users_in_project(request, projectID):
    project = project_api.get_project(projectID)
    if project is None:
        return redirect('/req/projects')
    association = UserAssociation.objects.get(
        user=request.user,
        project=project)
    users = project.users.all()
    pmusers = User.objects.filter(
        project__id=project.id,
        userassociation__role=user_association.ROLE_OWNER)
    devusers = User.objects.filter(
        project__id=project.id,
        userassociation__role=user_association.ROLE_DEVELOPER)
    cliusers = User.objects.filter(
        project__id=project.id,
        userassociation__role=user_association.ROLE_CLIENT)

    context = {
        'project': project,
        'association': association,
        'users': users,
        'pmusers': pmusers,
        'devusers': devusers,
        'cliusers': cliusers,
        'canOwnProject': request.user.has_perm(PERMISSION_OWN_PROJECT),
    }
    return render(request, 'UserList.html', context)


@login_required(login_url='/signin')
@user_owns_project()
def add_user_to_project(request, projectID, username):
    project = project_api.get_project(projectID)
    if request.method == 'POST':
        form = SelectAccessLevelForm(request.POST)
        if form.is_valid():
            user_role = (request.POST).get('user_role', '')
            project_api.add_user_to_project(projectID, username, user_role)
    else:
        form = SelectAccessLevelForm()

    users = user_manager.getActiveUsers()
    for puser in project.users.all():
        users = users.exclude(username=puser.username)
    context = {
        'title': 'Add User to Project',
        'form': form,
        'project': project,
        'users': users,
    }

    return render(request, 'UserSummary.html', context)


@login_required(login_url='/signin')
@user_owns_project()
def remove_user_from_project(request, projectID, username):
    project = project_api.get_project(projectID)
    if request.method == 'POST':
        form = SelectAccessLevelForm()
        project_api.remove_user_from_project(projectID, username)
    else:
        form = SelectAccessLevelForm()
    users = project.users.all()
    users = users.exclude(username=request.user.username)

    context = {
        'title': 'Remove User from Project',
        'form': form,
        'project': project,
        'users': users,
        'confirm_message': 'This is an unrevert procedure ! This user will lose the permission to access this project !',
    }

    return render(request, 'UserSummary.html', context)


@login_required(login_url='/signin')
@user_owns_project()
def manage_user_association(request, projectID, userID):
    form = SelectAccessLevelForm()
    the_project = project_api.get_project(projectID)
    the_user = User.objects.get(id=userID)
    association = UserAssociation.objects.get(
        user=the_user,
        project=the_project)
    role = association.role

    context = {
        'title': 'Change User Access Level',
        'form': form,
        'project': the_project,
        'user': the_user,
        'role': role,
    }
    return render(request, 'ManageUserAssociation.html', context)


@user_owns_project()
def change_user_role(request, projectID, userID):
    # Gets the project, user and role whose IDs have been passed to this view (the role
    # by POST) and passes them on to the project_api method of the same name.
    project = project_api.get_project(projectID)
    user = User.objects.get(id=userID)
    # print user.username #debug

    # Get the role that was sent via the dropdown in the form.
    retrieved_role = (request.POST).get('user_role')
    # print retrieved_role # to console for debugging
    project_api.change_user_role(project, user, retrieved_role)
    return redirect('/req/projectdetail/' + projectID)


@user_can_access_project()
def get_attachments(request, projectID):
    form = FileForm()
    context = {
        'form': form,
        'projectID': projectID,
        'referer': request.META['HTTP_REFERER'],
        'modalID': 'projAttachModal',
        'files': ProjectFile.objects.filter(project__id=projectID)
    }
    return render(request, 'Attachments.html', context)


@user_can_access_project()
def upload_attachment(request, projectID):

    if 'file' not in request.FILES:
        raise IOError("Missing file")
    if request.FILES['file'].size > 1100000:
        raise IOError("File too large")

    form = FileForm(request.POST, request.FILES)
    if(form.is_valid()):
        file = request.FILES['file']
        f = ProjectFile(
            project=project_api.get_project(projectID),
            file=file,
            name=file.name)
        f.save()
    return redirect(request.POST['referer'])


@user_can_access_project()
def download_file(request, projectID):

    file = ProjectFile.objects.get(
        project__id=projectID,
        name=request.GET.get(
            'file',
            ''))
    response = HttpResponse(file.file)
    response['Content-Disposition'] = 'attachment; filename=' + file.name
    return response
