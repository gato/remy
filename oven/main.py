from flask import Flask
from flask_restful import  Api
from oven.api import OvenAPI
import click


@click.command()
@click.option('--port', '-p', required=True, help='serving port ')

def command(port):

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(OvenAPI, '/oven', '/oven') 

    app.run(debug=True, host= '0.0.0.0', port=port)

command()