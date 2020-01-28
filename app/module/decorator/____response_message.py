from flask import request, jsonify, g
import logging

class ResponseMessage():
    """
    사용안함...
    """
    def __init__(self, fnc):
        self.__name__   = fnc.__name__
        self.fnc        = fnc
        self.logger     = logging.getLogger(self.__name__)


    def __call__(self, *args, **kwargs): 
        # logger = logging.getLogger(self.__name__)
        self.logger.debug('<< ResponseMessage Decorator >>')

        try:
            return self.fnc(*args, **kwargs)
        except Exception as e: 
            self.logger.exception(e)
            if request.is_xhr == True:
                g.error     = e
                return jsonify({
                    'success'   : False,
                    'message'   : "{}".format(e),
                })
            else:
                raise
