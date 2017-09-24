# Final_Project

## GETTING STARTED WITH LOCAL DEVELOPMENT IMAGE:
##### updated 9/24/2017 Dan Budris <dbudris@bu.edu>
Follow the steps in 'Deployment' to pull a Docker image of the development branch
Navigate to http://127.0.0.1:8080/admin for Django admin, or http://127.0.0.1:8080 for the system frontend
Log in with username admin, password pass

## MANAGEMENT:
### Django Management
##### updated 9/24/2017 Dan Budris <dbudris@bu.edu>
http://<project_url>/admin
http://127.0.0.1:8080/admin

The backend of the Project Management Tool is built in the Python framework Django.  Django provides a robust management interface for dealing with the backend of the project, including managing user accounts.  

#### Database
Django uses Sqlite3 as a database backend.  Sqlite 3 is a light-weight, file-based database which does not require a client application or any middleware.  Django writes directly to the database.  Currently, the master database is located at:
`/g1/database/db.sqlite3`


## DEPLOYMENT:
##### updated 9/24/2017 Dan Budris <dbudris@bu.edu>
### Automated Docker Build
There are two docker images maintained for this project, `danbudris/bu_met_cs673:latest` and `danbudris/bu_met_cs673:development`.
Docker builds are hosted on Docker Hub: https://hub.docker.com/r/danbudris/bu_met_cs673/builds/
Docker builds will trigger automatically when the Master or Development branch are updated.  Builds take about 8 minutes.
Latest will reflect the `Master` branch.  Development will reflect the `development` branch.

0. Install Docker (https://docs.docker.com/engine/installation/)
1. Pull the image from the Docker Hub
   1. `sudo docker pull danbudris/bu_met_cs673:development`
2. Start the docker image on your local host with the name cs673, mapping port 8080 to localhost port 8000.
   1. `docker run -d --name='cs673' -p 8080:8000 danbudris/bu_met_cs673:development`
3. Connect to the running application
   1. http://127.0.0.1:8080
   2. Or, you can connect to the container with a Bash shell to view the applicaiton code; `sudo docker exec -it cs673 bash`

### Manual, step by step instructions:
#### LEGACY INSTRUCTIONS: last updated by previous project group 2015
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
