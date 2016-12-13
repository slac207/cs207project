# Accessing the EC2 instance:
sudo ssh -i "metadata/cs207pair.pem" ubuntu@54.175.144.132

# Installs on the EC2 instance (though I think these should be in setup.py)
sudo pip3 install portalocker
sudo pip3 install pandas
sudo pip3 install scipy

# Disable firewall on EC2: 
sudo ufw disable

# Enter virtual environment
source ~/venvs/flaskproj/bin/activate

# Cloning the code base fresh
git clone https://github.com/slac207/cs207project.git
	
# Updating the code base
git pull origin master # or metadata (eventually we'll work from master)

# Going into our project folder
cd cs207project

# Running the database server from within the project folder
python3 ./TimeseriesDB/DatabaseServer.py

# Running the flask server from within the project folder
python3 ./metadata/rest.py

# Look at current running python processes
ps -ef | grep 'python'

# Enter into postgres - database ubuntu and user ubuntu
psql ubuntu ubuntu;
\d metadata; # describe metadata table
SELECT * FROM metadata; # get metadata table
\q # quit postgres
service postgresql status # check that postgres is active and see host

# Example Queries
http://54.175.144.132/timeseries # Query 1
http://54.175.144.132/timeseries/12 # Query 3
http://54.175.144.132/timeseries?mean_in=50-60 # Query 4
http://54.175.144.132/timeseries?level_in=A,B,C # Query 4
http://54.175.144.132/simquery/12 # Query 5
http://54.175.144.132/simquery/12?topn=10 # Query 5