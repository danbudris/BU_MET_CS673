FROM ubuntu:latest
MAINTAINER Dan Budris <dbudris@bu.edu>

RUN apt-get update -y
RUN apt-get install -y \
		       python2.7 \
                       python-pip \
                       curl \
                       wget \
                       git \
                       libncurses5-dev \
                       && pip install virtualenv

# make the base directories 
RUN mkdir ~/g1 && mkdir ~/g1/database && mkdir ~/g1/source && mkdir ~/g1/virtualenv && mkdir ~/g1/static

# clone the git repository to local
RUN git clone https://github.com/CS673S15-Group1/Final_Project ~/g1/source

# create the virtual environment and run the setup and database migration scripts
RUN virtualenv -p /usr/bin/python2.7 ~/g1/virtualenv && cd ~/g1/source/group1 && ../../virtualenv/bin/pip install -r ../dependencies.txt && ../../virtualenv/bin/python manage.py makemigrations && ../../virtualenv/bin/python manage.py migrate

EXPOSE 8000

CMD ["/root/g1/virtualenv/bin/python","/root/g1/source/group1/manage.py","runserver","0.0.0.0:8000"]
