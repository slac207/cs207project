mkdir ~/cs207project/
mkdir ~/cs207project/metadata/
cd ~/cs207project/metadata/

# to ~/flaskproj/flaskproj.py:
# a Flask file, such as:
echo '''from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:green'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0")''' > ~/cs207project/metadata/rest.py

    
# to ~/flaskproj/wsgi.py:
echo '''from rest import app

if __name__ == "__main__":
    app.run()''' > ~/cs207project/metadata/wsgi.py


#to ~/flaskproj/flaskproj.ini:
echo '''[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = flaskproj.sock
chmod-socket = 660
vacuum = true

die-on-term = true''' > ~/cs207project/metadata/flaskproj.ini

#sudo rm /etc/nginx/sites-available/default
#sudo rm /etc/nginx/sites-enabled/default

sudo systemctl start flaskproj
sudo systemctl enable flaskproj

sudo ln -s /etc/nginx/sites-available/flaskproj /etc/nginx/sites-enabled

sudo systemctl restart nginx
sudo ufw allow 'Nginx Full' 