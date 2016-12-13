
cd ~/cs207project/APIServer

printf "\n*******************************************************"
printf "\n Set up uWSGI"

# Crutch: make flask file
# cp rest.py rest_real.py
# cp ~/cs207project/provisioners/files/rest.py ./rest.py

# Entry point for wsgi into flask
cp ~/cs207project/provisioners/files/wsgi.py ./wsgi.py

# uWSGI setup file
cp ~/cs207project/provisioners/files/flaskproj.ini ./flaskproj.ini

# Setup file for running uWSGI as a systemd process
sudo cp ~/cs207project/provisioners/files/flaskproj.service /etc/systemd/system/flaskproj.service

# Start flaskproj as a systemd process
sudo systemctl start flaskproj
sudo systemctl enable flaskproj

# Check that wWSGI process is running properly
sudo systemctl status flaskproj


printf "\n*******************************************************"
printf "\n Set up nginx to communicate with uWSGI"

# Remove the nginx default site
sudo rm /etc/nginx/sites-enabled/default

# Make a server file for routing requests based on URI
sudo cp ~/cs207project/provisioners/files/flaskproj /etc/nginx/sites-available/flaskproj 
sudo ln -s /etc/nginx/sites-available/flaskproj /etc/nginx/sites-enabled

sudo systemctl restart nginx
sudo ufw allow 'Nginx Full' 
