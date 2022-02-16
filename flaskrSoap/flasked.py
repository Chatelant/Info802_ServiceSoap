import json
from flask import Flask, make_response, current_app


app = Flask(__name__)
app.config.from_object('settings')


# @app.route('/nimp')
# def hello():
#     '''Sample Flask API view that ruturns JSON with some data from config.
#     '''
#     response = make_response(json.dumps({
#         'nimp': current_app.config['ServiceVehicles'],
#     }))
#     response.headers['Content-Type'] = 'application/json'
#     return response
