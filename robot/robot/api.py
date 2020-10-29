from flask_restful import Resource, abort, reqparse
from http import HTTPStatus
from .model import get_robot

parser = reqparse.RequestParser()
parser.add_argument('command', type=str)
parser.add_argument('oven', type=int)

class RobotAPI(Resource):

    def post(self):
        # check if robot is already doing something
        if get_robot().busy():
            abort(HTTPStatus.CONFLICT, message='Robot is busy')
        args = parser.parse_args()
        # check if command is valid
        command = args['command']
        if not get_robot().valid_command(command):
            abort(HTTPStatus.BAD_REQUEST, message='command: "{}" not supported'.format(command))
        if not get_robot().valid_params(command, args):
            abort(HTTPStatus.BAD_REQUEST, message='missing mandatory parameter')
        get_robot().perform(command, args)
        return {'status': 'task started'}, HTTPStatus.CREATED

    def get(self):
        return {'status':  get_robot().get_task()}, HTTPStatus.OK

