#!/bin/bash
# CS207 AWS EC2 Ubuntu 16.04 instance provisioning script (for final project)
# Installs final project stack: numpy, Flask, SQL Alchemy, nginx, and PostgreSQL
# Also configures firewall for nginx HTTP access, starts nginx server,
# and runs basic checks to ensure installation completed and services started.

# show the current Python 3 version (if any)
python3 --version

# update / upgrade the current software libraries
sudo apt-get update
sudo apt-get --upgrade

# install Python3 pip and development essentials + the psycopg2 library for PostgreSQL access
printf "\n*******************************************************"
printf "\nInstalling virtualenv, python3-pip, python3-dev, and psycopg2 ...\n"
sudo apt-get install virtualenv python3-pip python3-dev python3-psycopg2

# "~" specifies the AWS EC2 instance home directory for virtual environment
cd ~
mkdir venvs

# use the AWS EC2 Ubuntu 16.04 instance python3 installation
virtualenv --python=/usr/bin/python3 venvs/flaskproj

printf "\n*******************************************************"
printf "\nUpgrading pip ...\n"
pip3 install --upgrade pip

# install numpy for Python3
printf "\n*******************************************************"
printf "\nInstalling numpy ...\n"
pip3 install numpy

printf "\n*******************************************************"
printf "\nInstalling Flask and SQL Alchemy ...\n"
source ~/venvs/flaskproj/bin/activate

# install flask and SQLAlchemy for Python3
sudo pip3 install flask Flask-SQLAlchemy


# install PostgreSQL
printf "\n*******************************************************"
printf "\nInstalling PostgreSQL ...\n"
sudo apt-get install postgresql postgresql-contrib
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

printf "\nCan import numpy, Flask, SQLAlchemy, and psycopg2 in Python3?\n"
sudo python3 cs207_aws_ec2_stack_test.py

printf "\nIs nginx running?\n"
sudo service nginx status


printf "\nFINISHED!\n"
