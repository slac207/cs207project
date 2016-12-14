# CS207 AWS EC2 Ubuntu 16.04 instance provisioning script

# Make the shell scripts executable
chmod a+x *.sh

# Install components
~/cs207project/provisioners/install_components.sh

# Run database server as a systemd process
~/cs207project/provisioners/dbserver.sh

# Populate postgres database
~/cs207project/provisioners/postgres_setup.sh

# Connect nginx with Flask via wWSGI
~/cs207project/provisioners/nginx-flask.sh

# Burn-in the postgres database
python3 ~/cs207project/provisioners/files/burn_in.py

# Confirm that installation worked
~/cs207project/provisioners/status.sh
