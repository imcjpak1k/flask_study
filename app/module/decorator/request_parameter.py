from flask import request, jsonify
import logging

class RequestParameter():
    def __init__(self, fnc):
        self.__name__   = fnc.__name__
        self.fnc        = fnc
        self.logger     = logging.getLogger(self.__name__)

    def __call__(self, *args, **kwargs): 
        self.logger.debug('<< RequestParameter Decorator >>')
        self.logger.debug("\tfunction name :  {}".format( self.fnc.__name__) )
        self.logger.debug("\t - json_data :{} ".format( request.get_json()) )
        self.logger.debug("\t - is_xhr :{} ".format( request.is_xhr) )
        self.logger.debug("\t - form :{} ".format( request.form) )
        self.logger.debug("\t - args :{} ".format( request.args) )
        
        return self.fnc(*args, **kwargs)
