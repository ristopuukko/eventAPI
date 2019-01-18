from flask import Flask, request, jsonify
from bson import ObjectId
import requests as req
import socket 
import db
import time 
import random
import json

app = Flask(__name__)

dbase = db.Db()

# testing ipaddresses 
# ipaddresses = [
# '12.87.118.0',
# '64.17.254.216',
# '65.23.121.221',
# '67.43.156.0',
# '67.43.156.64',
# '78.26.70.208',
# '81.2.69.160',
# '82.99.17.96',
# '83.206.36.224',
# '85.88.2.224',
# '89.160.20.112',
# '142.217.214.0',
# '222.230.136.0'
# ]


ERROR_REQ_FORMAT = 'Please check your data request format.\n'
ERROR_REQ_FORMAT += ' city=[cityname]&st=[starttime]&et=[endtime]\n'
ERROR_REQ_FORMAT += ' time format :  \"%Y-%m-%d:%H.%M.%S\" \n'
ERROR_REQ_FORMAT += ' for example : curl \'http://ec2-34-201-52-248.compute-1.amazonaws.com:5000?city=Stockholm&st=2019-1-17:09.01.00&et=2019-1-17:09.02.30\'\n'


def getlocation(geoservice=None, ipaddress=None):
    '''fetch the remote host location
    '''
    url='http://'+geoservice+':8080/info?ip='+ipaddress
    r = req.get(url)
    jsonstr=r.text
    locdict = json.loads(jsonstr)

    if r.status_code == 429:
        timetosleep = float(locdict['period_remaining'])
        time.sleep(timetosleep)
        getlocation(geoservice, ipaddress)


    result=str()
    try:
        result=locdict['city']
    except:
        result='N/A'

    return result

def gethostname(ipaddress=None):
    '''use the socket to try and get the remote hostname
    '''
    try: 
        host_name = socket.gethostbyaddr(ipaddress) 
    except: 
        host_name = 'n/a'

    return host_name[0]

@app.route('/findevent', methods=['GET'])
def findevent():
    '''create a query for city & timerange 
    '''
    result=str()
    if request.method == 'GET':
        if 'city' in request.args and 'st' in request.args and 'et' in request.args:
            cityname = str(request.args.get('city')).upper()
            time_start=request.args.get('st')
            time_end=request.args.get('et')
        else:
            return 'Bad Request', 400

        data = dbase.get(cityname, time_start, time_end)

        if data[:10]=='ValueError':
            result = 'Bad Request', 400

        elif data[:10]=='queryError':
            result = 'Not Found', 404

        else:
            result = data, 200


    else:

        result = 'Bad Request', 400


    return result


@app.route('/event', methods=['POST'])
def event():
    '''write the JSON paylaod to the db 
    '''

    geoservice = 'geoipapi'
    # geoservice = '127.0.0.1' # DEBUG 

    try:
        jsonpayload = request.get_json(force=True)

    except:
        return  'input data has to be in JSON-format', 400

    remoteaddr = request.remote_addr
    # remoteaddr = ipaddresses[random.randint(0,len(ipaddresses)-1)] # DEBUG
    remotehost = gethostname(remoteaddr)

    if len(remotehost)<3:
        remotehost='N/A'
    
    result = '', 400
    
    location=getlocation(geoservice, remoteaddr)
    
    if len(location)<4 or location=='N/A':
        result ='JSON payload saved but cannot fetch the location for this ip : {}'.format(remoteaddr), 200
    
    written = dbase.set(remoteaddr, remotehost, location, jsonpayload)
    
    if written:
        result = 'Ok', 200
    
    return result

    



@app.route('/')
def index():
    return 'you\'ve reached my events application!'


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
