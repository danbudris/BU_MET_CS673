"""Common utility functions.
"""
import datetime
import random

from django.contrib.auth.models import User
from django.db import IntegrityError
from issue_tracker import models as it_models
from requirements.models import project_api
from requirements.models import user_association as user_association_model

USERS = (('Mike', 'Bibriglia', 'mbibrigl',),
         ('Bill', 'Cosby', 'bcosby',),
         ('John', 'Stewart', 'jstewart',),
         ('John', 'Oliver', 'joliver',),
         ('Stephen', 'Colbert', 'scolbert',),
         ('Conan', 'Obrien', 'teamcoco',),
         ('Tina', 'Fey', 'thirtyrockfey',),
         ('George', 'Carlin', 'gcarlin',),
         ('Jonny', 'Carson', 'jcarson',),
         ('George', 'Burns', 'jburns',),
         ('Whitney', 'Cummings', 'whitcummings',),
         ('Daniel', 'Tosh', 'tosho',),
         ('Kevin', 'Hart', 'khart',),
         ('Lucille', 'Ball', 'lball',),
         ('Rosanne', 'Barr', 'rbarr',),
         ('Billy', 'Crystal', 'bcrystal',),
         ('Robin', 'Williams', 'aladin',),
         ('Jim', 'Carrey', 'mask4ever',),
         ('Dave', 'Chappelle', 'threeseason',),
         ('Ellen', 'DeGeneres', 'ellen',),
         ('Jeff', 'Foxworthy', 'mightberedneck',),
         ('Zach', 'Galifanakis', 'twoferns',),
         ('Whoopi', 'Goldberg', 'whoopi',),
         ('Jimmy', 'Fallon', 'fallon',),
         ('Andy', 'Kaufman', 'manonmoon',),
         ('Jay', 'Leno', 'leno',),
         ('Denis', 'Leary', 'dleary',),
         ('Steve', 'Martin', 'crazywildguy',),
         )

DESCRIPTIONS = (
    "Everybody let's go. Go. \nJump up, wiggle and giggle with the "
    "Mother Goose Club. \nI'm Teddy, \nI'm Eep, \nI'm Baa Baa Sheep. \n"
    "'m Mary,\nI'm Jack, \nI'm Little Bo Peep. \nEverybody let's go. Go. \n"
    "Sing a song, we'll all sing along with the Mother Goose Club. \n"
    "The Mother Goose Club.",
    "Clap your hands.\nClap your hands.\nClap them just like me.\n\n"
    "Touch your shoulders.\nTouch your shoulders.\n"
    "Touch them just like me.\n\n"
    "Pat your knees.\nPat your knees.\nPat them just like me.\n\n"
    "Stomp your feet.\nStomp your feet.\nStomp them just like me.\n\n"
    "Clap your hands.\nClap your hands.\nNow let them quiet be.\n",)

TITLES = (
    "I stole a pot.",
    "core dump on the mainframe of my dashboard.",
    "Swallowed the cat to catch the bird, swallowed the bird"
    " to catch the spider, but no spider caught",
    "Man thrown on cart claims not to be dead yet.",
    "I got an A in CS 673, but deserved an A+.",
    "But I shot a man in reno, just to watch him die.",
    "Living on a prayer, but expected to be living on a pension.",
    "Not sleeping well enough. Should sleep through night.",
    "I have fallen, and I cannot get up.",
    "Everything is broken.",
    "General. Failing. Help",
    "Another random bug.",
    "I want my bikeshed painted BLUE though!",
    )

COMMENTS = (
    "I just wanted to say all of this stuff is a buncha hooey.",
    "Legal has agreed with me that this is actually not an issue."
    "  Please close.",
    "I have considered carefully everything you said and discarded it"
    " as both non-factual and fool-hearty.  Next time try to appeal to my"
    " cold rational brain.",
    "This is an automated statement: 42.",
    "I forgot to say in the description.. What a wonderful world.",
    )

PROJECTS = (
    ("Issue tracking project",
     "We must go deeper into creating issues for project managing by creating"
     " a project to manage the issue tracking."),
    ("Project management",
     "Ever see a snake eat its tail?"),
    ("Communication",
     "Tell me all about it!"),
    ("Dummy Project!",
     "Sorta like the book series. You can learn a lot from a dummy!"),
    ("Big Ole Project",
     "It is about this big. *makes hand gesture*"),
    )


def create_user(first, last, username, out_handle=None):
    """Create the django super user account.

    Args:
      first: First name.
      last: Last name.
      username: User handle.
      out_handle: The output handler for printing.
    """
    try:
        user_pw = "{}pw".format(username)
        user = User.objects.create_user(username=username,
                                        email='%s@bu.edu' % username,
                                        password=user_pw,
                                        **{'first_name': first,
                                           'last_name': last})
        user.save()
    except Exception as e:
      print e
    except IntegrityError as e:
        print e
        if out_handle:
            out_handle.write(
                'User already exists, skipping creation: %s' % username)


def create_users(users, out_handle=None):
    """Create some number of users

    Args:
      users: A tuple of tuples containing first name, last name and user.
      out_handle: The output handler for printing.
    """
    if out_handle:
        out_handle.write('\nCreating users...')
    for full_user in users:
        (first, last, username) = full_user
        create_user(first, last, username, out_handle)


def create_super_user(first, last, username, out_handle=None):
    """Create the django super user account.

    Args:
      first: First name.
      last: Last name.
      username: User handle.
      out_handle: The output handler for printing.
    """
    if out_handle:
        out_handle.write('\nCreating Super User...')
    try:
        super_user_pw = "{}pw".format(username)
        user = User.objects.create_superuser(username,
                                             email='%s@bu.edu' % username,
                                             password=super_user_pw,
                                             **{'first_name': first,
                                                'last_name': last})
        user.save()
    except Exception as e:
        print e
    except IntegrityError as e:
        print e
        if out_handle:
            out_handle.write('User already exists, skipping creation: %s'
                             % username)


def get_random_date():
    return datetime.datetime.now() + datetime.timedelta(
        days=random.randint(-365, 365))


def create_issues(number_of_issues, out_handle=None):
    """Creating some number of random issues.

    The issues will start in various states with random assignees.

    Args:
      num: The number of issues to be created.
      out_handle: The output handler for printing.
    """
    try:
        project_ids = []
        for project in project_api.get_all_projects():
            project_ids.append(project.pk)
        title_count = len(TITLES) - 1
        description_count = len(DESCRIPTIONS) - 1
        if out_handle:
            out_handle.write('\nCreating issues')
        for _ in xrange(number_of_issues):
            if out_handle:
                out_handle.write('.', ending='')
                out_handle.flush()
            # Go through a few extra hoops to make sure that if we create a issue
            # with any status other than new, it has been assigned to someone.
            status = it_models.STATUSES[
                random.randint(0, len(it_models.STATUSES) - 1)][0]
            p = project_api.get_project(
                project_ids[random.randint(0, len(project_ids) - 1)])
            # Limit the users to the developers on the project
            user_ids = [user_ass.user.pk
                        for user_ass in project_api.get_project_users(p.id)]
            if status != 'new':
                assignee = User.objects.get(
                    pk=user_ids[random.randint(0, len(user_ids) - 1)])
            else:
                assignee = None
            if random.randint(0, 1):
                verifier = None
            else:
                verifier = User.objects.get(
                    pk=user_ids[random.randint(0, len(user_ids) - 1)])

            issue = it_models.Issue.objects.create(
                title=TITLES[random.randint(0, title_count)],
                description=DESCRIPTIONS[
                    random.randint(0, description_count)],
                issue_type=it_models.TYPES[
                    random.randint(0, len(it_models.TYPES) - 1)][0],
                status=status,
                priority=it_models.PRIORITIES[
                    random.randint(0, len(it_models.PRIORITIES) - 1)][0],
                project=p,
                modified_date=get_random_date(),
                submitted_date=get_random_date(),
                reporter=User.objects.get(
                    pk=user_ids[random.randint(0, len(user_ids) - 1)]),
                assignee=assignee,
                verifier=verifier,
                )
            comment_count = len(COMMENTS) - 1
            for _ in xrange(1, random.randint(1, 10)):
                it_models.IssueComment.objects.create(
                    comment=COMMENTS[random.randint(0, comment_count)],
                    issue_id=issue,
                    date=get_random_date(),
                    poster=User.objects.get(
                        pk=user_ids[random.randint(0, len(user_ids) - 1)]),
                    is_comment=True)

        if out_handle:
            out_handle.write('\n')
    except Exception as e:
        print e


def _get_random_user(user_ids):
    return User.objects.get(pk=user_ids[random.randint(0, len(user_ids) - 1)])


def create_projects(number_of_projects, out_handle=None):
    """Creating some number of random projects

    The projects will start in various states with different user associations.

    Args:
      number_of_projects: The number of projects to be created.
      out_handle: The output handler for printing.
    """
    # This extra work for user ids is necessary due to the fact that the
    # database might have been wiped, but the origin pk for the user still
    # has been claimed, so we must gather the current pk list to apply them
    # to create issues.
    try:
        user_ids = []
        for user in User.objects.all():
            user_ids.append(user.pk)
        user_count = len(user_ids) - 1
        project_count = len(PROJECTS) - 1
        if out_handle:
            out_handle.write('\nCreating projects')
        for i in xrange(number_of_projects):
            if out_handle:
                out_handle.write('.', ending='')
                out_handle.flush()
            fields = {'title': '%s: %d' % (
                          PROJECTS[random.randint(0, project_count)][0],
                          i),
                      'description': PROJECTS[random.randint(0, project_count)][1]}
            excluded_users = [_get_random_user(user_ids)]
            p = project_api.create_project(user=excluded_users[0],
                                           fields=fields)

            # Now associate some number of developers to the project.
            for _ in xrange(random.randint(1, user_count)):
                # Remove the users already associated with the project
                ids = set(user_ids) - set([user.pk for user in excluded_users])
                u = _get_random_user(list(ids))
                excluded_users.append(u)
                project_api.add_user_to_project(
                    p.id, u.username, user_association_model.ROLE_DEVELOPER)

        if out_handle:
            out_handle.write('\n')
    except Exception as e:
        print e

def wipe_db():
    """This will wipe the database of all Users and Issues."""
    User.objects.all().delete()
    it_models.Issue.objects.all().delete()
