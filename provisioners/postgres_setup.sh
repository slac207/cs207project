cd ~/cs207project
source ~/venvs/flaskproj/bin/activate
# Delay for 2 seconds to wait for the server setup to make the files.
python delay.py
# Populate the postgres database.
python ./APIServer/postgres_test_metadata.py