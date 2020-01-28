from flask import render_template, jsonify, request, session
import logging

class LoginRequired():
    def __init__(self, fnc):
        self.__name__   = fnc.__name__
        self.fnc        = fnc
        self.logger     = logging.getLogger(self.__name__)


    def __call__(self, *args, **kwargs): 
        # logger = logging.getLogger(self.__name__)
        self.logger.debug('<< LoginRequired Decorator >>') 

        if 'user_info' not in session:
            if request.is_xhr == True:
                return jsonify({'message' : '로그인 후 시도하여 주십시오.'})
            else:
                return render_template("login.html")

        return self.fnc(*args, **kwargs)

# def login_required(func):
#     """
#     로그인인증 체크
#     """
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if 'user_info' not in session:
#             if request.is_xhr == True:
#                 return jsonify({'message' : '로그인 후 시도하여 주십시오.'})
#             else:
#                 return render_template("login.html")
#         return func(*args, **kwargs)
#     return wrapper


