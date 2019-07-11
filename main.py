import smartcar
import credentials as c
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
        client_id=c.cred["CLIENT_ID"],
        client_secret=c.cred["CLIENT_SECRET"],
        redirect_uri=c.cred["REDIRECT_URI"],
        test_mode=False,
        )

@app.route('/', methods=['GET'])
def helloWorld():
    return 'helloWorld\n'


@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)

@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    global access
    access = client.exchange_code(code)

    return "exchange_succesful"

@app.route('/unlock', methods=['GET'])
def unlock():

    response = smartcar.get_vehicle_ids(access['access_token'])
    print("", response)
    vehicle = smartcar.Vehicle(response["vehicles"][0], access['access_token'])
    print(vehicle)

    res = vehicle.unlock()
    print(res)

    return jsonify(res)

@app.route('/lock', methods=['GET'])
def lock():

    response = smartcar.get_vehicle_ids(access['access_token'])
    print(response)
    vehicle = smartcar.Vehicle(response["vehicles"][0], access['access_token'])
    print(vehicle)

    res = vehicle.lock()
    print(res)

    return jsonify(res)



@app.route('/info', methods=['GET'])
def info():
    
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']

    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()

    print(info)

    return jsonify(info)

@app.route('/odo', methods=['GET'])
def odo():
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']

    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'], unit_system = "imperial")

    odometer = vehicle.odometer()

    return jsonify(odometer)
@app.route('/loc', methods = ['GET'])
def location():
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    loc = vehicle.location()
    return jsonify(loc)

if __name__ == '__main__':
    app.run(port=80)
