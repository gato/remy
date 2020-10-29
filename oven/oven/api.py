from flask_restful import Resource, abort
from http import HTTPStatus
from .model import get_oven

class OvenAPI(Resource):

    def post(self):
        # place Pizza in oven
        # check if oven empty  
        if not get_oven().empty:
            abort(HTTPStatus.CONFLICT, message='Oven is not empty')
        get_oven().place_pizza()
        return {'status':'cooking started'}, HTTPStatus.CREATED

    def delete(self):
        # pick pizza from oven
        # check if oven empty  
        if get_oven().busy():
            abort(HTTPStatus.CONFLICT, message='Oven is still cooking')
        if get_oven().empty:
            abort(HTTPStatus.CONFLICT, message='Oven is empty')
        get_oven().pick_pizza()
        return None, HTTPStatus.NO_CONTENT

    def get(self):
        status = 'idle'
        if get_oven().busy():
            status = 'busy'
        elif get_oven().empty:
            status = 'empty'
        return {'status': status}, HTTPStatus.OK
        

