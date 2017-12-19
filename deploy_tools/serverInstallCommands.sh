#!/usr/bin/env bash
#Tested on Ubuntu 14.04 LTS x64 - logged in as root
#check os
lsb_release -irc
#check kernel release
uname -or
#add user for programming enviroment
adduser pgmvt
#review users
cat /etc/passwd
# give sudo to pgmvt
usermod -a -G sudo pgmvt
#check groups of user
groups pgvmt
##
## EXIT AND LOGIN AS pgmvt
##
#update package manager links
sudo apt-get update
#install finger application
sudo apt-get install finger
#install tree application
sudo apt-get install tree
#check user attributes
finger pgmvt
#make directory for downloads
mkdir ~/downloads
#change directory to downloads
cd ~/downloads
#install development tools
sudo apt-get install build-essential
#**********************INSTALL PYTHON2.7.9 (UPGRADE B/C IT EXISTS IN UBUNTU)************
#install dependencies
sudo apt-get install libbz2-dev libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev build-essential libsqlite3-dev bzip2 libbz2-dev libncurses5-dev cmake bison libreadline-dev libxml2-dev libeditline-dev libaio-dev
#download source python files
curl -LOk https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
#untar compressed python file
tar -xvf Python-2.7.9.tgz
#change directory to decompressed python direcotry
cd Python-2.7.9/
#configure installation of python34
sudo ./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
#install python (must be installed as root --altinstall to configure another python2.7.9 and pip2.7 vs python2.7 would be the executable shortcut (unix link) in path)
sudo make && sudo make altinstall
#change directory to downloads
cd ~/downloads
###download setuptools -- required for python27, in python34 is already included
curl -LOk https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
###install setup tools
sudo python2.7 ez_setup.py
###install pip
sudo easy_install-2.7 pip
#upgrade pip
sudo -H pip2.7 install --upgrade pip
#***************************SETUP VIRTUALENV*******************************************
#install virtualenv
sudo apt-get install python-virtualenv
#*******************************SETUP GIT**********************************************
#install dependencies
sudo apt-get install libbz2-dev libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev build-essential libsqlite3-dev bzip2 libbz2-dev libncurses5-dev cmake bison libreadline-dev libxml2-dev libeditline-dev libaio-dev
#change directory to downloads
cd ~/downloads
#download the tar file
curl -LOk https://www.kernel.org/pub/software/scm/git/git-2.3.5.tar.gz
#untar the file
tar -xvf git-2.3.5.tar.gz
#change directory to decompressed git
cd git-2.3.5/
#make install
sudo make prefix=/usr/local install
# change directory to home
cd ~
# download git-completion bash file for autocomplete in git
curl -LOk https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash
#add git autocomplete
sudo vim ~/.bashrc
#add the folowing lines
source ~/git-completion.bash
#update bashrc
source ~/.bashrc
#**********************INSTALL NODEJS***************************************************
#install nodejs
sudo apt-get install nodejs
#**********************INSTALL NGINX***************************************************
#remove previously installed nginx
sudo apt-get remove nginx
sudo apt-get remove nginx-core
sudo apt-get remove nginx-common
#install dependencies
sudo apt-get install libc6 libpcre3 libssl0.9.8 zlib1g lsb-base libpcre3 libpcre3-dev
#change directory to downloads
cd ~/downloads
#download nginx stable
curl -LOk http://nginx.org/download/nginx-1.6.3.tar.gz
#untar compressed nginx file
tar -xvf nginx-1.6.3.tar.gz
#cd into nginx dir
cd nginx-1.6.3
#configure installation of nginx
./configure --sbin-path=/usr/local/sbin --with-http_ssl_module
#sample return output
##Configuration summary
##  + using system PCRE library
##  + using system OpenSSL library
##  + md5: using OpenSSL library
##  + sha1: using OpenSSL library
##  + using system zlib library
##
##  nginx path prefix: "/usr/local/nginx"
##  nginx binary file: "/usr/local/sbin"
##  nginx configuration prefix: "/usr/local/nginx/conf"
##  nginx configuration file: "/usr/local/nginx/conf/nginx.conf"
##  nginx pid file: "/usr/local/nginx/logs/nginx.pid"
##  nginx error log file: "/usr/local/nginx/logs/error.log"
##  nginx http access log file: "/usr/local/nginx/logs/access.log"
##  nginx http client request body temporary files: "client_body_temp"
##  nginx http proxy temporary files: "proxy_temp"
##  nginx http fastcgi temporary files: "fastcgi_temp"
##  nginx http uwsgi temporary files: "uwsgi_temp"
##  nginx http scgi temporary files: "scgi_temp"
#make and install
sudo make && sudo make install
#start nginx and test by going to the server's ip in a browser http://45.55.238.181
sudo /usr/local/sbin/nginx
#stop nginx
sudo kill `cat /usr/local/nginx/logs/nginx.pid`
#create init file
sudo vim /etc/init.d/nginx
#enter the following shell script
################################################################################################################
################################################################################################################
################################################################################################################
#! /bin/sh

### BEGIN INIT INFO
# Provides:          nginx
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the nginx web server
# Description:       starts nginx using start-stop-daemon
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/local/sbin/nginx
NAME=nginx
DESC=nginx

test -x $DAEMON || exit 0

# Include nginx defaults if available
if [ -f /etc/default/nginx ] ; then
    . /etc/default/nginx
fi

set -e

. /lib/lsb/init-functions

case "$1" in
  start)
    echo -n "Starting $DESC: "
    start-stop-daemon --start --quiet --pidfile /usr/local/nginx/logs/$NAME.pid \
        --exec $DAEMON -- $DAEMON_OPTS || true
    echo "$NAME."
    ;;
  stop)
    echo -n "Stopping $DESC: "
    start-stop-daemon --stop --quiet --pidfile /usr/local/nginx/logs/$NAME.pid \
        --exec $DAEMON || true
    echo "$NAME."
    ;;
  restart|force-reload)
    echo -n "Restarting $DESC: "
    start-stop-daemon --stop --quiet --pidfile \
        /usr/local/nginx/logs/$NAME.pid --exec $DAEMON || true
    sleep 1
    start-stop-daemon --start --quiet --pidfile \
        /usr/local/nginx/logs/$NAME.pid --exec $DAEMON -- $DAEMON_OPTS || true
    echo "$NAME."
    ;;
  reload)
      echo -n "Reloading $DESC configuration: "
      start-stop-daemon --stop --signal HUP --quiet --pidfile /usr/local/nginx/logs/$NAME.pid \
          --exec $DAEMON || true
      echo "$NAME."
      ;;
  status)
      status_of_proc -p /usr/local/nginx/logs/$NAME.pid "$DAEMON" nginx && exit 0 || exit $?
      ;;
  *)
    N=/etc/init.d/$NAME
    echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
    exit 1
    ;;
esac

exit 0
################################################################################################################
################################################################################################################
################################################################################################################
#make the file an executable
sudo chmod +x /etc/init.d/nginx
#add the script to the default run levels
sudo /usr/sbin/update-rc.d -f nginx defaults
#service nginx start/stop/restart
sudo service nginx start
## MIRORRING DEBIAN STYLE FOLDER LAYOUT SETUP
#create folders
sudo mkdir /usr/local/nginx/sites-available
sudo mkdir /usr/local/nginx/sites-enabled
#configuration letting nginx know where sites-enabled for virtual hosts (vhosts)
sudo vim /usr/local/nginx/conf/nginx.conf
#enter the following shell script
################################################################################################################
################################################################################################################
################################################################################################################
user www-data;
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;

    keepalive_timeout  65;

    gzip  on;

    include /usr/local/nginx/sites-enabled/*;

}
################################################################################################################
################################################################################################################
################################################################################################################
#restart the server
sudo service nginx restart
#**********************3BLUEPRINTS PM SETUP***************************************************
# export variable to remove searching for www.3bleuprints site folder
## make sure you replace 'dev', with 'pre' or 'pro' or 'www' as needed
export SITENAME=www.3blueprints.com
# create directory structure
mkdir -p ~/sites/$SITENAME/database
mkdir -p ~/sites/$SITENAME/source
mkdir -p ~/sites/$SITENAME/static
mkdir -p ~/sites/$SITENAME/virtualenv
# clone in project
git clone https://github.com/CS673S15-Group1/Final_Project ~/sites/$SITENAME/source/
# create virtual enviroment for project
virtualenv --python=python2.7 ~/sites/$SITENAME/virtualenv
# install dependencies
~/sites/$SITENAME/virtualenv/bin/pip2.7 install -r ~/sites/$SITENAME/source/dependencies.txt
# create and run migrations
~/sites/$SITENAME/virtualenv/bin/python2.7 ~/sites/$SITENAME/source/group1/manage.py makemigrations
~/sites/$SITENAME/virtualenv/bin/python2.7 ~/sites/$SITENAME/source/group1/manage.py migrate
#edit the file into the sites-available of nginx
sudo vim /usr/local/nginx/sites-available/$SITENAME
#add the following configuration
server {
    listen 80;
    server_name www.3blueprints.com;

    location / {
        proxy_pass http://localhost:8000;
    }
}
#enable the site by creating a symlink into the sites enabled of nginx
sudo ln -s /usr/local/nginx/sites-available/$SITENAME /usr/local/nginx/sites-enabled/$SITENAME
#restart nginx
sudo service nginx restart
###################; visit http://www.3blueprints.com
~/sites/$SITENAME/virtualenv/bin/python2.7 ~/sites/$SITENAME/source/group1/manage.py createsuperuser
~/sites/$SITENAME/virtualenv/bin/python2.7 ~/sites/$SITENAME/source/group1/manage.py runserver
#change directory to where the wsgi application from django is placed
cd ~/sites/$SITENAME/source/group1
#test that gunicorn runs; visit http://www.3blueprints.com (no css/static files)
sudo ../../virtualenv/bin/gunicorn group1.wsgi:application
#to make nginx serve static files edit the following file
sudo vim /usr/local/nginx/sites-available/$SITENAME
#replace with the following lines
server {
    listen 80;
    server_name www.3blueprints.com;

    location / {
        proxy_pass http://localhost:8000;
    }

    location /static {
        alias /home/pgmvt/sites/www.3blueprints.com/static;
     }
}
# send all django project static files to main static folder
~/sites/$SITENAME/virtualenv/bin/python2.7 ~/sites/$SITENAME/source/group1/manage.py collectstatic
#reload nginx
sudo service nginx reload
#restart gunicorn to test (with static service); visit http://www.3blueprints.com
sudo ../../virtualenv/bin/gunicorn group1.wsgi:application
#to make nginx use sockets
sudo vim /usr/local/nginx/sites-available/$SITENAME
#replace with the following lines
server {
    listen 80;
    server_name www.3blueprints.com;

    location / {
        proxy_set_header Host $host;
        proxy_pass http://unix:/tmp/www.3blueprints.com.socket;
    }

    location /static {
        alias /home/pgmvt/sites/www.3blueprints.com/static;
     }
}
#reload nginx
sudo service nginx reload
#restart gunicorn to test (with socket binding); visit http://www.3blueprints.com
sudo ../../virtualenv/bin/gunicorn --bind unix:/tmp/www.3blueprints.com.socket group1.wsgi:application
#**********************GUNICORN UPSTART CONFIG***************************************************
#finally we automate the gunicorn by using ubuntu's upstart init
sudo vim /etc/init/gunicorn-www.3blueprints.com.conf
#add the following lines
description "Gunicorn server for www.3blueprints.com"

start on net-device-up
stop on shutdown

respawn

setuid root
chdir /home/pgmvt/sites/www.3blueprints.com/source/group1

exec ../../virtualenv/bin/gunicorn --bind unix:/tmp/www.3blueprints.com.socket group1.wsgi:application

#start gunicorn (will comeback up if machine goes down
sudo stop gunicorn-www.3blueprints.com
sudo start gunicorn-www.3blueprints.com
#**********************NODEJS UPSTART CONFIG***************************************************
#alter absolute paths (2 lines) in the main.js file to the correct server path relative to the project directory
##(may not be required if www.3blueprints.com) #TODO: change to relative paths
vim ~/home/pgmvt/sites/www.3blueprints.com/source/group1/communication/node/main.js
#finally we automate the nodejs by using ubuntu's upstart init
sudo vim /etc/init/nodejs-www.3blueprints.com.conf
#add the following lines
description "NodeJS server for www.3blueprints.com"

start on net-device-up
stop on shutdown

respawn

setuid root

exec node /home/pgmvt/sites/www.3blueprints.com/source/group1/communication/node/main.js

#start gunicorn (will comeback up if machine goes down
sudo stop nodejs-www.3blueprints.com
sudo start nodejs-www.3blueprints.com
#check the status of the services
sudo service --status-all | grep nginx
initctl list | grep nodejs
initctl list | grep gunicorn
#**********************INSTALL MYSQL5.6***************************************************
#add user for programming enviroment
sudo adduser mysql
#review users
cat /etc/passwd
# give sudo to pgmvt
sudo usermod -a -G sudo mysql
#check groups of user
groups mysql
##
## EXIT AND LOGIN AS mysql
##
#login as mysql to install MYSQL5
#make directory for mysql in /usr/local
sudo mkdir /usr/local/mysql
#make directory for mysql download in /usr/local/mysql/1dload
sudo mkdir /usr/local/mysql/1dload
#change directory ownership to mysql
sudo chown -R mysql:mysql /usr/local/mysql
#change directory to mysql download
cd /usr/local/mysql/1dload
#transfer mysql source file from host OR download from web
curl -LOk http://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.24.tar.gz
#untar file in 1dload
tar -xvf mysql-5.6.24.tar.gz
#download make dependencies
sudo apt-get install build-essential libncurses5-dev cmake bison libreadline-dev libxml2-dev libeditline-dev libaio-dev
#change directory decompressed directory
cd mysql-5.6.24
#cmake the file
cmake /usr/local/mysql/1dload/mysql-5.6.24
#make and install the file
make install /usr/local/mysql/1dload/mysql-5.6.24
#change directory to mysql scripts
cd /usr/local/mysql/scripts
#execute installation script
sudo ./mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data
#copy server start file to init.d
sudo cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql
#edit system profile to add mysql path to the system path (/etc/profile)
sudo vim /etc/profile
#add the following lines
export PATH=$PATH:/usr/local/mysql/bin
#source the file to  take effect
source /etc/profile
#start mysql
service mysql start
#change directory to mysql bin
cd /usr/local/mysql/bin
#execute secure installation script (mysql hardening)
./mysql_secure_installation
#login with root (with apache installed you must indicate the host connection with -h)
mysql -u root -p - h 127.0.0.1
#check version
select version();
##review databases
SHOW DATABASES;
#review tables in default privileges and authentication database (mysql)
SHOW TABLES IN mysql;
#select all users
select user,host,password from mysql.user;
#create user for mysql admin
CREATE USER mysql IDENTIFIED BY 'password';
#grant all access to mysql adming
GRANT ALL ON *.* TO 'mysql'@'%';
#show columns of mysql.user tables
show columns from mysql.user;
#select all users
select user,host,password from mysql.user;
#review general user privileges
select user,select_priv,update_priv,grant_priv from mysql.user;
# create m6db database
CREATE DATABASE group1;
# set database encoding to utf-8
ALTER DATABASE group1 CHARACTER SET utf8 COLLATE utf8_general_ci;
#review user privilege statement record
show grants for mysql;
#review user privilege at database level
select DB,user,select_priv,insert_priv,update_priv from mysql.db
