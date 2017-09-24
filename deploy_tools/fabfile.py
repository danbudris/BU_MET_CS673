from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.contrib.files import append
from fabric.contrib.files import exists
from fabric.contrib.files import sed
import random

REPO_URL = 'https://github.com/CS673S15-Group1/Final_Project'


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/group1/group1/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s", "localhost"]' % (site_name,)
       )
    secret_key_file = source_folder + '/group1/group1/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python2.7 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/dependencies.txt'
        % (virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    run('cd %s/group1 &&'
        ' ../../virtualenv/bin/python2 manage.py collectstatic --noinput'
        % (source_folder,))


def _update_database(source_folder):
    run('cd %s/group1 &&'
        ' ../../virtualenv/bin/python2 manage.py makemigrations'
        % (source_folder,))
    run('cd %s/group1 &&'
        ' ../../virtualenv/bin/python2 manage.py migrate --noinput'
        % (source_folder,))
