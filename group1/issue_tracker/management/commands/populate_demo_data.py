"""Script for populating demo users.

THIS SCRIPT IS FOR DEVELOPMENT PURPOSES ONLY.

To run:
        python manage.py populate_demo_data
"""
import optparse

from django.core.management.base import BaseCommand
from issue_tracker import utils


class Command(BaseCommand):
    """A command for populating the database with demo data/users."""

    option_list = BaseCommand.option_list + (
        optparse.make_option(
            '--issues', action='store', type='int',
            dest='issues', default=1000,
            help='The number of random issues to populate the db with.'),
        optparse.make_option(
            '--projects', action='store', type='int',
            dest='projects', default=100,
            help='The number of random projects to populate the db with.'),
        )

    def handle(self, *args, **options):
        """Where the command magic happens."""
        utils.create_users(users=utils.USERS, out_handle=self.stdout)
        utils.create_super_user(first='Super', last='Woman',
                                username='test', out_handle=self.stdout)
        utils.create_projects(number_of_projects=options['projects'],
                              out_handle=self.stdout)
        utils.create_issues(number_of_issues=options['issues'],
                            out_handle=self.stdout)
