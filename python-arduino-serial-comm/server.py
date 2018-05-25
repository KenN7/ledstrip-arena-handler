from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import json
import sched
import time
import asyncio

import experimentctrl as ec

app = Flask(__name__)

@app.route('/arena-handler/api/v1.0/state', methods=['POST'])
def setState():
    if not request.json or not 'arena' in request.json:
        abort(400)
    ec.runState(request.json)
    return jsonify({"response":"good"}), 201

@app.route('/arena-handler/api/v1.0/experiment', methods=['POST'])
async def setExperiment():
    data =  await request.json()
    if not request.json or not 'arena' in request.json:
        abort(400)
    ec.runState(request.json)
    return jsonify({"response":"good"}), 201

if __name__ == '__main__':
     app.run(port=5002)