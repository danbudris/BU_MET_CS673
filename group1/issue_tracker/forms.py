"""Collection of forms used by the issue tracker."""
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from issue_tracker.models import STATUSES
from issue_tracker.models import TYPES
from issue_tracker.models import PRIORITIES
from issue_tracker import models as it_models
from requirements.models import project as project_model


class EmptyChoiceField(forms.ChoiceField):
    """Class to provide a means of having an empty value defaulted.

    Class taken from Gist.
      - https://gist.github.com/davidbgk/651080
    """
    def __init__(self, choices=(), empty_label=None, required=True,
                 widget=None, label=None, initial=None, help_text=None,
                 *args, **kwargs):
        # prepend an empty label if it exists (and field is not required!)
        if not required and empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))
        super(EmptyChoiceField, self).__init__(
            choices=choices, required=required, widget=widget, label=label,
            initial=initial, help_text=help_text, *args, **kwargs)


class SearchForm(forms.Form):
    """Search for issues based on provided criteria."""
    title = forms.CharField(
        required=False,
        help_text='Substring matching in issue title.')
    description = forms.CharField(
        required=False,
        help_text='Substring matching in the long description.')
    status = EmptyChoiceField(choices=STATUSES, required=False, empty_label='')
    issue_type = EmptyChoiceField(choices=TYPES, required=False,
                                  empty_label='')
    priority = EmptyChoiceField(choices=PRIORITIES, required=False,
                                empty_label='')
    project = forms.ModelChoiceField(
        queryset=project_model.Project.objects.all(), required=False)

    # TODO(jdarrieu) Need to look into how to get this hooked up.
    # Date based filtering still not working.
    submitted_date = forms.DateField(
        help_text='Date issue was created. (mm/dd/yyyy)',
        required=False,
        input_formats=['%m/%d/%Y', '%m-%d-%Y'])
    modified_date = forms.DateField(
        help_text='Date issue was last modified. (mm/dd/yyyy)',
        required=False,
        input_formats=['%m/%d/%Y', '%m-%d-%Y'])
    closed_date = forms.DateField(
        help_text='Date issue was closed. (mm/dd/yyyy)',
        required=False,
        input_formats=['%m/%d/%Y', '%m-%d-%Y'])

    reporter = forms.ModelChoiceField(queryset=User.objects.all(),
                                      required=False)
    assignee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      required=False)
    verifier = forms.ModelChoiceField(queryset=User.objects.all(),
                                      required=False)


class CommentForm(ModelForm):
    class Meta:
        model = it_models.IssueComment
        fields = '__all__'
