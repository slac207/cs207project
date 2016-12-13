
source ~/venvs/flaskproj/bin/activate

printf "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
printf "\n*******************************************************"

printf "\nAre packages properly installed?"
python check_imports.py

printf "\n\n\nIs nginx running?\n"
sudo service nginx status

printf "\n\n\nIs DBServer running?\n"
sudo systemctl status dbserver

printf "\n\n\nIs uWSGI running?\n"
sudo systemctl status flaskproj
