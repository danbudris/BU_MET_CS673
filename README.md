# Final_Project

###### note: locally, you must install nodejs and run main.js in /communication/node/main.js for the communication application to work; also adjust the 2 absolute paths in the main.js file to match the directory structure

### LOCAL INSTALLATION (windows systems)
###### to use linux style commands of this README please install git bash (http://www.geekgumbo.com/2010/04/09/installing-git-on-windows/)
##### create a directory in your drive C:
##### 
mkdir /c/g1
##### 
mkdir /c/g1/database
##### 
mkdir /c/g1/source
##### 
mdkir /c/g1/virtualenv
##### 
mkdir /c/g1/static

##### clone project into source folder
git clone https://github.com/CS673S15-Group1/Final_Project /c/g1/source

##### create a virtual environment
###### note: must have installed python 2.7 to the default directory in C:\Python27
###### note: must have virtual env installed 'pip install virtualenv' -- must have pip installed, usually included on windows system installs
virtualenv -p /c/Python27/python.exe /c/g1/virtualenv

##### change directory to the project source
cd /c/g1/source/group1

##### install dependencies 
###### note: windependencies file for windows since readline is not compatible, may have to change all 'import readline' to 'import pyreadline as readline'
../../virtualenv/Scripts/pip.exe install -r ../windependencies.txt

##### make the migration files
../../virtualenv/Scripts/python.exe manage.py makemigrations

##### run the database migration
../../virtualenv/Scripts/python.exe manage.py migrate

##### run server, navigate to http://localhost:8000 in a browser
../../virtualenv/Scripts/python.exe manage.py runserver


### LOCAL INSTALLATION (*nix systems [Mac, Ubuntu...])
##### create a directory in your home directory
##### 
mkdir ~/g1
##### 
mkdir ~/g1/database
##### 
mkdir ~/g1/source
##### 
mkdir ~/g1/virtualenv
##### 
mkdir ~/g1/static
##### clone project into source folder
git clone https://github.com/CS673S15-Group1/Final_Project ~/g1/source

##### create a virtual environment
###### note: must have installed python 2.7 to the default directory in /usr/local/bin with a python2.7 executable via altinstall
###### note: must have virtual env installed 'pip install virtualenv' -- must have pip installed, usually included on windows system installs
###### note: see server installation script under deploy_tools for details on installing a new python
virtualenv -p /usr/local/bin/python2.7 ~/g1/virtualenv

##### change directory to the project source
cd ~/g1/source/group1

##### install dependencies
../../virtualenv/bin/pip install -r ../dependencies.txt

##### make the migration files
../../virtualenv/bin/python manage.py makemigrations

##### run the database migration
../../virtualenv/bin/python manage.py migrate

##### run server, navigate to http://localhost:8000 in a browser
../../virtualenv/bin/python manage.py runserver


### SERVER INSTALLATION (*nix systems)
###### note: follow the commands under deploy_tools serverInstallcommands.sh (not tested as an executable shell script)
###### note: must have fabric installed (on windows this will require a manual installation (setup_py) of pycrypto first, you may find pre-compiled windows binaries here (http://www.voidspace.org.uk/python/modules.shtml#pycrypto)
##### change directory to where deploy_tools is on your local computer - this script is deployed from your local computer to the server
cd /c/g1/source/deploy_tools
###### note: must activate virtualenv with fabric (you may have fabric installed on your path python, and not require a virtualenv)
##### run the fabfile.py script with the following command to upload the project from origin/master to the specified server
fab deploy:host=pgmvt@dev.3blueprints.com
