
printf "\n*******************************************************"
print "\n Set up database server as a systemd process"

# Setup file for running DBserver as a systemd process
sudo cp ~/cs207project/provisioners/files/dbserver.service /etc/systemd/system/dbserver.service

# Start DBserver as a systemd process
sudo systemctl start dbserver
sudo systemctl enable dbserver

# Check that DBserver is running properly
sudo systemctl status dbserver