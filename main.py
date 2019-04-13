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

# TODO: Authorization Step 1a: Launch Smartcar authorization dialog


@app.route('/login', methods=['GET'])
def login():
    # TODO: Authorization Step 1b: Launch Smartcar authorization dialog
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    # TODO: Authorization Step 3: Handle Smartcar response
    code = request.args.get('code')

    global access
    access = client.exchange_code(code)

    return '', 200

    # TODO: Request Step 1: Obtain an access token


@app.route('/unlock', methods=['GET'])
def unlock():
    # TODO: Request Step 2: Get vehicle ids
    global access

    response = smartcar.get_vehicle_ids(access['access_token'])
    print(response)
    vehicle = smartcar.Vehicle(response["vehicles"][0], access['access_token'])
    print(vehicle)

    res = vehicle.unlock()
    print(res)

    return jsonify(res)

@app.route('/lock', methods=['GET'])
def lock():
    # TODO: Request Step 2: Get vehicle ids
    global access

    response = smartcar.get_vehicle_ids(access['access_token'])
    print(response)
    vehicle = smartcar.Vehicle(response["vehicles"][0], access['access_token'])
    print(vehicle)

    res = vehicle.lock()
    print(res)

    return jsonify(res)



@app.route('/info', methods=['GET'])
def info():
    # TODO: Request Step 2: Get vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']

    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()

    print(info)

    return jsonify(info)

    # TODO: Request Step 3: Create a vehicle
    
    # TODO: Request Step 4: Make a request to Smartcar API



if __name__ == '__main__':
    app.run(port=8000)
