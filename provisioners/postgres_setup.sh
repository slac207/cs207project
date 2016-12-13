cd ~/cs207project
source ~/venvs/flaskproj/bin/activate
# Delay for 3 seconds to wait for the server setup to make the files.
sleep 3
# Populate the postgres database.
python ./APIServer/postgres_test_metadata.py