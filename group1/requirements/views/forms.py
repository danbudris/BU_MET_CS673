from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from django.forms.extras.widgets import SelectDateWidget, Select
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from requirements.models import user_association
from requirements.models.project import Project
from requirements.models.story import Story
from requirements.models.task import Task
from requirements.models.iteration import Iteration
from requirements.models.story_comment import StoryComment
from django.forms.models import inlineformset_factory
import re

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # ensure that the password meets our new security standards
        password_test = re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$', password1);
        if not password_test:
            raise forms.ValidationError('Your password must be at least 8 characters long and must '
            'contain at least one uppercase letter, one lowercase letter, and one number.')
        return self.cleaned_data.get("password1")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # ensure that the user is signing up with a BU email account
        email_test = re.match(r'^[A-Za-z0-9\.\+_-]+@bu\.edu$', email)
        if not email_test:
            raise forms.ValidationError('You must register with a BU email acocunt to use this site.')
        return self.cleaned_data.get("email")     

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.is_active = True # should be false once email validation is finished 
        if commit:
            user.save()
        return user


class ChangePwdForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordChangeForm, self).__init__(self.user, *args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})


class UserProfileForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')


class IterationForm(forms.ModelForm):

    def __init__(self, *args, ** kwargs):
        super(IterationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_end_date(self):
        startdate = self.cleaned_data['start_date']
        enddate = self.cleaned_data['end_date']
        if enddate < startdate:
            raise forms.ValidationError(
                'Iteration end date should be later than it\'s start date !')
        return enddate

    class Meta:
        model = Iteration
        fields = ('title', 'description', 'start_date', 'end_date',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.TextInput(attrs={'readonly': 'readonly'}),
            'end_date': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Project
        fields = ('title', 'description',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class SelectAccessLevelForm(forms.Form):
    # Dropdown list to select from one of the current access levels for a
    # project.
    user_role = forms.ChoiceField(choices=(
        (user_association.ROLE_CLIENT, "Client"),
        (user_association.ROLE_DEVELOPER,
         "Developer"),
        (user_association.ROLE_OWNER,
         "Owner"),
    ), widget=Select(attrs={'class': 'form-control'}))


class StoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop(
            'project',
            None)  # retrive the parameter project, then call the superclass init
        super(StoryForm, self).__init__(*args, **kwargs)
        # change the origin field 'owner' to ChoiceField
        self.fields['owner'] = forms.ModelChoiceField(
            queryset=self.project.users.all(),
            empty_label='None',
            required=False)
        # add 'form-control' into all element's class attrtribute
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_hours(self):
        data = self.cleaned_data['hours']
        if data < 0:
            raise forms.ValidationError(
                'Hours should be greater than or equal to 0 !')
        return data

    class Meta:
        model = Story
        fields = (
            'title',
            'description',
            'reason',
            'test',
            'hours',
            'owner',
            'status',
            'points',
            'pause')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'reason': forms.Textarea(attrs={'rows': 5}),
            'test': forms.Textarea(attrs={'rows': 5}),
        }


class FileForm(forms.Form):
    file = forms.FileField(
        widget=ClearableFileInput(
            attrs={
                'class': 'form-control'}))

# class registrationForm(forms.Form):
# 	firstName = forms.CharField(label='First Name:', max_length=100)
# 	lastName = forms.CharField(label='Last Name:', max_length=100)
# 	emailAddress=forms.CharField(label='Email Address:', max_length=100)
# 	username=forms.CharField(label='Username:', max_length=100)
# 	password=forms.CharField(label='password:', max_length=100, widget=forms.PasswordInput())
# 	confirmPassword=forms.CharField(label='Confirm password:', max_length=100)


class CommentForm(forms.ModelForm):

    def __init__(self, *args, ** kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = StoryComment
        fields = ('title', 'comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class TaskForm(forms.ModelForm):

    def __init__(self, *args, ** kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Task
        fields = ('description',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1}),
        }

TaskFormSet = inlineformset_factory(
    Story,
    Task,
    fields=(
        'description',
    ),
    form=TaskForm,
    extra=0)
