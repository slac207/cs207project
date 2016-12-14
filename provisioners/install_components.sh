# Installs stack: numpy, Flask, SQL Alchemy, nginx, uwsgi, PostgreSQL

# update / upgrade the current software libraries
sudo apt-get update
sudo apt-get --upgrade

# install Python3 pip and development essentials + the psycopg2 library for PostgreSQL access
printf "\n*******************************************************"
printf "\nInstalling virtualenv, python3-pip, python3-dev, and psycopg2 ...\n"
sudo apt-get install virtualenv python3-pip python3-dev python3-psycopg2 libpq-dev

printf "\n*******************************************************"
printf "\nUpgrading pip ...\n"
pip3 install --upgrade pip

# set up a virtual environment
cd ~
mkdir venvs
sudo chown -R ubuntu:ubuntu ~/venvs
virtualenv --python=/usr/bin/python3 venvs/flaskproj
source ~/venvs/flaskproj/bin/activate

# Install our package
printf "\n*******************************************************"
printf "\nInstall CS207 project packages ...\n"
cd ~/cs207project
pip install -e .
#python setup.py install

# install numpy, scipy, pandas, portalocker
printf "\n*******************************************************"
printf "\nInstalling numpy, scipy, pandas, portalocker ...\n"
pip install numpy scipy pandas portalocker 
#psycopg2

# install flask and SQLAlchemy
printf "\n*******************************************************"
printf "\nInstalling Flask and SQL Alchemy ...\n"
pip install flask Flask-SQLAlchemy uwsgi numpy

# install PostgreSQL
printf "\n*******************************************************"
printf "\nInstalling PostgreSQL ...\n"
sudo apt-get install postgresql postgresql-contrib

# set-up a Postgres table;
printf "\n*******************************************************"
printf "\nAt the postgres =# prompt, enter the following commands:\n"
printf "alter user postgres password 'password'; create user ubuntu createdb createuser password 'cs207password'; create database ubuntu owner ubuntu; \q"
sudo -u postgres psql
echo "PostgreSQL installed"

# install and configure nginx
printf "\n*******************************************************"
printf "\nInstalling and starting nginx ...\n"
sudo apt-get install nginx
sudo service nginx start

printf "\nConfiguring firewall for nginx HTTP access ...\n"
sudo ufw app list # show current firewall settings
sudo ufw allow 'Nginx HTTP' # allow nginx to use HTTP port
printf "\nAfter configuring firewall for nginx HTTP access ...\n"
sudo ufw status

echo "nginx installed and configured \n"

# Installation should be complete and services started
# Run checks to be sure
printf "\n*******************************************************"
printf "\nINSTALLATION AND SERVICE CHECKS ...\n"
printf "\n*******************************************************"


printf "\nFINISHED!\n"

deactivate
