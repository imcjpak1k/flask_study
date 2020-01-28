import os
import sys
import logging
from flask import Blueprint, request, session, jsonify, g
# 비밀번호 hash
# from werkzeug import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)

this = Blueprint('user', __name__, url_prefix='/user')

sys.path.append(sys.path[0])
from app.business import user as user_biz
from app.module.decorator.login_required import LoginRequired
from app.module.decorator.request_parameter import RequestParameter


@this.route('/test')
def test():
    return "test page"

@this.route('/login', methods=['POST', 'GET'])
@RequestParameter
def login():
    """
    사용자 로그인 인증
    """
    logger.debug("<<< login try >>>")
    # request param
    json_data   = request.get_json(silent=True, cache=False, force=True)

    id = json_data.get('id', '')
    pw = json_data.get('pw', '')

    logger.debug(  """
                     id : {id}
                     pw : {pw}
                    """.format(id=id, pw=pw)
    )

    # validation check                
    if len(id) == 0 or len(pw) == 0 :
        raise RuntimeError("아이디/비밀번호를 입력하여 주십시오.")

    # user_biz
    user_data   = user_biz.login(id, pw)
    
    # session 등록
    session['user_info'] = user_data

    return jsonify(user_data)
    


@this.route('/logout', methods=['POST', 'GET'])
@LoginRequired
def logout():
    session.clear()
    # return "logout page"
    return jsonify( {'message' : '정상적으로 로그아웃 하였습니다.',
                     'success' : True
                    })  
