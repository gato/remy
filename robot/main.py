from flask import Flask
from flask_restful import  Api
from robot.api import RobotAPI
from robot.model import configure_robot, BEFORE_ROLE, AFTER_ROLE
import click


@click.command()
@click.option('--port', '-p', required=True, help='serving port ')
@click.option('--role', '-r', required=True, help='Robot Role [before|after]')

def command(port, role):
    role = role.lower()
    if role not in ['before', 'after']:
        print('invalid role {} valid values are [before|after]'.format(role))
        return

    role = BEFORE_ROLE if role == 'before' else AFTER_ROLE
    configure_robot(role)

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(RobotAPI, '/robot', '/robot') 

    app.run(debug=True, host= '0.0.0.0', port=port)

command()
