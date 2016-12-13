# CS207 AWS EC2 Ubuntu 16.04 instance provisioning script

# Make the shell scripts executable
chmod a+x *.sh

# Install components
~/cs207project/provisioners/install_components.sh

# Connect nginx with Flask via wWSGI
~/cs207project/provisioners/nginx-flask.sh

# Run database server as a systemd process
~/cs207project/provisioners/dbserver.sh

