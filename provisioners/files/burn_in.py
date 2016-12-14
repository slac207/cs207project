import sys, requests

# Get the public IP
pubIP = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
url_base = 'http://'+pubIP.text+'/timeseries/'

for i in range(100):
    requests.get(url_base+str(i))
    