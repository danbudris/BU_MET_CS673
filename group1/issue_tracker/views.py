"""Container for the various views supported."""
import datetime

from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from issue_tracker import forms
from issue_tracker import models as it_models
from issue_tracker import filters
from django.core.urlresolvers import reverse


class CreateIssue(CreateView):
    model = it_models.Issue
    fields = ['title', 'description', 'issue_type', 'priority', 'project',
              'assignee']
    template_name = 'create_issue.html'

    # new_issue.date_modified should be new_issue.date_submitted.

    def form_valid(self, form):
        new_issue = form.save(commit=False)
        new_issue.reporter = self.request.user
        new_issue.date_modified = datetime.datetime.now()
        new_issue.save()
        return HttpResponseRedirect(new_issue.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(CreateIssue, self).get_context_data(**kwargs)
        AddUserCountsToContext(context, self.request.user)
        return context


class EditIssue(UpdateView):
    model = it_models.Issue
    fields = ['title', 'description', 'issue_type', 'priority', 'project',
              'assignee', 'status', 'verifier']
    template_name = 'edit_issue.html'

    def form_valid(self, form):
        if form.has_changed():
            current_issue = form.save(commit=False)
            text = ['Issue is modified:']
            issue = it_models.Issue.objects.get(pk=self.object.pk)
            for field_name, field in form.fields.items():
                if field_name in form.changed_data:
                    # if field_name in ['assignee', 'verifier']:
                    #     text.append('%s: old value -> %s' % (
                    #         field_name,
                    #         form.cleaned_data[field_name].username))
                    # I don't know how to make it more easy to read(Amy)
                    if field_name == 'assignee':
                        if issue.assignee is None:
                            assignee = None
                        else:
                            assignee = issue.assignee.username
                        if form.cleaned_data[field_name] is None:
                            username = None
                        else:
                            username = form.cleaned_data[field_name].username
                        text.append('%s: %s -> %s' % (
                            field_name, assignee, username))
                    elif field_name == 'verifier':
                        if issue.verifier is None:
                            verifier = None
                        else:
                            verifier = issue.verifier.username
                        if form.cleaned_data[field_name] is None:
                            username = None
                        else:
                            username = form.cleaned_data[field_name].username
                        text.append('%s: %s -> %s' % (
                            field_name, verifier, username))
                    else:
                        text.append('%s: %s -> %s' % (
                            field_name,
                            getattr(issue, field_name),
                            form.cleaned_data[field_name]))

            current_issue.save()
            new_comment = it_models.IssueComment(comment='\n'.join(text),
                                                 issue_id=self.object,
                                                 poster=self.request.user,
                                                 date=datetime.datetime.now(),
                                                 is_comment=False)
            new_comment.save()
        return HttpResponseRedirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(EditIssue, self).get_context_data(**kwargs)
        AddUserCountsToContext(context, self.request.user)
        return context


class ViewIssue(DetailView, FormMixin):
    model = it_models.Issue
    template_name = 'issue_detail.html'
    form_class = forms.CommentForm

    def get_context_data(self, **kwargs):
        context = super(ViewIssue, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['comment_list'] = it_models.IssueComment.objects.filter(
            issue_id=self.object).order_by('-date')
        # context['form'] = forms.CommentForm
        context['form'] = self.get_form(form_class)

        AddUserCountsToContext(context, self.request.user)
        return context

    def get_success_url(self):
        return reverse('view_issue', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        new_comment.issue_id = self.object
        new_comment.poster = self.request.user
        new_comment.date = datetime.datetime.now()
        new_comment.is_comment = True
        new_comment.save()
        return super(ViewIssue, self).form_valid(form)
        # return HttpResponseRedirect(new_comment.get_absolute_url())


class SearchIssues(FormView):
    form_class = forms.SearchForm
    template_name = 'search.html'
    success_url = '/issue/search/'

    def get_context_data(self, **kwargs):
        context = super(SearchIssues, self).get_context_data(**kwargs)
        AddUserCountsToContext(context, self.request.user)
        return context

    def form_valid(self, form, **kwargs):
        data = filters.filter_issue_results(form.cleaned_data)
        if not data:
            data = []
            # error = 'No Data'  # error text message
            SearchListCount = 0
        else:
            # ----------------------------------------
            SearchListCount = data.count()
        # ----------------------------------------
        context = self.get_context_data(**kwargs)
        context['object_list'] = data
        context['page'] = 'Issue Search'
        context['Seacount'] = SearchListCount
        return self.render_to_response(context)
        # ----------------------------------------

    # TODO(Ted): I add this but it does not work
    # def form_invalid(self, form):
    #     data = filters.filter_issue_results(form.cleaned_data)
    #     if not data:
    #         data = []
    #         error = 'No Data'
    #         # return super(SearchIssues, self).form_valid(form)

    #     return self.render_to_response({'object_list': data,
    #                                     'page': 'Issue Search',
    #                                     'form': form,
    #                                     'NoDataError': error,
    #                                     })
    #     return super(SearchIssues, self).form_invalid(form)
    # testing form_invalid funcation


class MultipleIssues(ListView):
    model = it_models.Issue
    template_name = 'multi_issue.html'

    def get_context_data(self, **kwargs):
        context = super(MultipleIssues, self).get_context_data(**kwargs)
        AddUserCountsToContext(context, self.request.user)
        return context


class AssigneeListIssuesView(MultipleIssues):

    def get_queryset(self):
        queryset = it_models.Issue.objects.filter(
            assignee=self.request.user).filter(
                status__in=[x[0] for x in it_models.OPEN_STATUSES])
        return queryset


class ReporterListIssuesView(MultipleIssues):

    def get_queryset(self):
        queryset = it_models.Issue.objects.filter(
            reporter=self.request.user).order_by('-pk')
        return queryset


class ClosedListIssuesView(MultipleIssues):

    def get_queryset(self):
        queryset = it_models.Issue.objects.filter(
            status__in=[x[0] for x in it_models.CLOSED_STATUSES]).order_by(
                '-closed_date')
        return queryset


class VerifiedListIssuesView(MultipleIssues):

    def get_queryset(self):
        queryset = it_models.Issue.objects.filter(
            verifier=self.request.user).order_by('-pk')
        return queryset


def AddUserCountsToContext(context, user):
    """Add user counts to the context.

    This work serves to add various different counts to the context so that
    the left sidebar can display the counts specific to each user.  Please note
    that this method adds 4 new elements to the context dict.

    Args:
      context: The context dictionary for the request.
      user: The use object provided with the request.
    """
    context['Asscount'] = it_models.Issue.objects.filter(
        assignee=user).filter(
            status__in=[x[0] for x in it_models.OPEN_STATUSES]).count()
    context['Repcount'] = it_models.Issue.objects.filter(
        reporter=user).order_by('-pk').count()
    context['Clocount'] = it_models.Issue.objects.filter(
        status__in=[x[0] for x in it_models.CLOSED_STATUSES]).order_by(
            '-closed_date').count()
    context['Vercount'] = it_models.Issue.objects.filter(
        verifier=user).order_by('-pk').count()
