from flask import Flask, render_template, request, session, json, jsonify, g
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler
import mybatis_mapper2sql
import logging
import os
import sys

sys.path.append(sys.path[0])
from config import DevelopmentConfig as cfg 
from app.model.models import db
from app.module import date_util
from app.module.decorator.login_required import LoginRequired
from app.module.decorator.unique_key import UniqueKey
from app.module.request_util import get_req_data
# from app.business.stock_symbol_scraping import stock_symbol_load_all

# 파일로 남기기 위해  filename='test.log' parameter로 추가한다.
# logging.basicConfig(filename='/logs/test.log', level=logging.DEBUG)
logging.basicConfig(  
                    # filename=cfg.LOG_PATH, 
                      level=cfg.LOG_LEVEL
                    )
logger = logging.getLogger(__name__)
# sqlalchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(cfg.LOG_LEVEL)
logging.getLogger('sqlalchemy.pool').setLevel(cfg.LOG_LEVEL) 
logging.getLogger('pool_echo').setLevel(cfg.LOG_LEVEL) 
logging.getLogger('sqlalchemy.orm').setLevel(cfg.LOG_LEVEL)

# # Bcrypt(암호알고리즘)
# bcrypt = None

def create_app(): 
    """
    flask app생성
    pytest-flask 라이브러리로 테스트 진행시 사용하는 Flask객체를 반환함.
    """
    flask_app = Flask(__name__)

    # Config
    flask_app.config.from_object('config.Config') 

    # SQLAlchemy
    db.init_app(flask_app)

    # Bcrypt
    # bcrypt = Bcrypt(flask_app)

    # scheduler
    scheduler = APScheduler()
    scheduler.init_app(flask_app)
    scheduler.start()

    try:
        import importlib
        with flask_app.app_context():
            for blueprint in flask_app.config['BLUEPRINTS']:
                module = importlib.import_module(blueprint)
                flask_app.register_blueprint(module.this)
    except Exception as e:
        logger.exception(e)
        raise   
    
    

    return flask_app

# flask app create
app = create_app()

# Bcrypt(암호알고리즘)
bcrypt = Bcrypt(app)

# MyBatis
mapper, xml_raw_text = mybatis_mapper2sql.create_mapper(xml=cfg.MYBATIS_PATH)

# # scheduler
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()


def get_flask_app():
    return app

def get_scheduler():
    return app.apscheduler

def get_mybatis_mapper():
    return mapper

def get_bcrypt():
    # return Bcrypt(get_flask_app())
    return bcrypt

@app.before_first_request
def before_first_request():
    logger.debug("<< before_first_request >>")
    logger.debug("<< before_first_request >>")
    logger.debug("<< before_first_request >>")
    logger.debug("앱이 기동되고 나서 첫 번째 HTTP 요청에만 응답")

@app.before_request
def before_request():
    logger.debug("<< before_request >>")
    logger.debug("<< before_request >>")
    logger.debug("<< before_request >>")
    logger.debug('request.path : {}'.format(request.path))
    # logger.debug(get_scheduler())
    # logger.debug(get_scheduler())
    # logger.debug(get_scheduler())
    # logger.debug(get_scheduler())


    g.error     = None
    g.is_error  = False
                                    
    g.user_info             = session.get('user_info', None)
    g.request_dtm           = date_util.current_datetime()
    g.current_fmt           = date_util.current_date_fmt()
    g.current_datetime_fmt  = date_util.current_datetime_fmt()
    g.apl_dtm               = date_util.current_date_fmt()      # 적용일시(이력데이터조회 사용)

    # request 적용일시 
    req_data    = request.get_json(silent=True, cache=True, force=True)
    if req_data != None and len(req_data) > 0:  
        apl_dtm     = req_data.get('_APL_DTM_')
    else:   
        apl_dtm     = get_req_data('_APL_DTM_')
    
    if apl_dtm != None and len(apl_dtm) > 0:
        g.apl_dtm   = apl_dtm      # 적용일시(이력데이터조회 사용)



@app.after_request
def after_request(response):
    logger.debug("<< after_request >>")
    logger.debug("<< after_request >>")
    logger.debug("<< after_request >>")
    logger.debug(response)
    return response


@app.teardown_request
def teardown_request(exception):
    logger.debug("<< teardown_request >>")
    logger.debug("<< teardown_request >>")
    logger.debug("<< teardown_request >>")
    if exception is not None: logging.debug(exception)


@app.teardown_appcontext
def teardown_appcontext(exception):
    logger.debug('<< teardown_appcontext >>')
    logger.debug('<< teardown_appcontext >>')
    logger.debug('<< teardown_appcontext >>')
    if exception is not None: 
        logging.exception(exception)

    req_dtm = g.request_dtm
    res_dtm = date_util.current_datetime()
    svc_timedetail  = res_dtm - req_dtm
    logger.debug(
        f'''
        << 서비스 시간 >>
        - request  time : {req_dtm}
        - response time : {res_dtm}
        - service  time : {svc_timedetail.seconds} sec, {svc_timedetail.microseconds} ms
        ''')

    # try:
    #     # Database Connection commit/rollback
    #     # SQLALCHEMY_COMMIT_ON_TEARDOWN = True 인 경우에는 아래 db.session.commit, rollback를 안해주면 아래오류메세지 발생
    #     # net:ERR_CONTENT_LENGTH_MISMATCH
    #     is_error = g.get('is_error', False)
    #     error = g.get('error', '')
    #     if is_error == True:
    #         db.session.rollback()
    #     else:
    #         db.session.commit()
    # except Exception as e:
    #     logging.exception(e)
    # finally:
    #     req_dtm = g.request_dtm
    #     res_dtm = date_util.current_datetime()
    #     svc_timedetail  = res_dtm - req_dtm
    #     logger.debug(
    #         f'''
    #         << 에러여부 >>
    #         - Error Yn : {is_error}
    #         - Error    : {error}
    #         << 서비스 시간 >>
    #         - request  time : {req_dtm}
    #         - response time : {res_dtm}
    #         - service  time : {svc_timedetail.seconds} sec, {svc_timedetail.microseconds} ms
    #         ''')
    
    

@app.errorhandler(Exception)
def internal_error(error):
    logger.debug('<< Internal Server Error >>') 
    logger.debug('<< Internal Server Error >>') 
    logger.debug('<< Internal Server Error >>') 
    logger.exception(error)
    
    # sqlalchemy.exc.IntegrityError
    # Databse Rollback처리
    db.session.rollback()

    if request.is_xhr == True:
        return jsonify({
            'success'   : False,
            'message'   : "{}".format(error),
        })
    return str(error) 


@app.errorhandler(404)
def page_not_found(error):
    logger.debug('<< page_not_found >>') 
    logger.debug('<< page_not_found >>') 
    logger.debug('<< page_not_found >>') 
















# @app.teardown_appcontext
# def teardown_appcontext(exception):
#     logger.debug('<< teardown_appcontext >>')
#     if exception is not None: logging.exception(exception)

#     # Database Connection commit/rollback
#     if hasattr(g, 'conn'):
#         conn        = g.conn
#         if conn is not None and not conn._closed:
#             try:
#                 is_error = g.get('is_error', False)
#                 if is_error == True:
#                     # conn.rollback()
#                     db.session.rollback()
#                 else:
#                     db.session.commit()
#             except:
#                 pass
#             finally:
#                 pass


# @app.errorhandler(404)
# def page_not_found(error):
#     logger.debug('<< page_not_found >>') 


# @app.errorhandler(Exception)
# def internal_error(error):
#     logger.debug('<< Internal Server Error >>') 
#     logger.debug(type(error))
#     logger.exception(error)

#     # error 추가
#     g.error     = error
#     g.is_error  = True
    
#     if request.is_xhr == True:
#         return jsonify({
#             'success'   : False,
#             'message'   : "{}".format(error),
#         })
    
#     return str(error)







@app.route('/')
@LoginRequired
def index():
    # from app.model.models import User
    # user = User.query.filter_by(email='imcjpak1k@naver.com')
    # logger.debug(user.all())
    # logger.debug(scoped_session(session_maker))
    # logger.debug(scoped_session(session_maker))
    # logger.debug(scoped_session(session_maker))
    """
    기본페이지이동
    """
    return "index page "





@app.route('/<page_id>', methods=['GET', 'POST'])
@LoginRequired
def forward_page(page_id):
    """
    flaskr.py를 제외한 모든 route는 2 depth를 사용하도록 한다.
    """
    logger.debug("\n\n<<< 화면이동 >>>")
    resources           = app.config.get('PAGE_LIST')
    page_resource       = resources.get(page_id)    
    logger.debug(f'요청ID : {page_id}, 페이지정보 : {page_resource}')
    
    if page_resource == None or len(page_resource) == 0:
        raise FileNotFoundError("요청하신 페이지정보가 존재하지 않습니다.")

    template        = page_resource.get('template')
    template_title  = page_resource.get('title')


    args = {}
    if request.method == 'GET':
        args    = dict(request.args)
    else :
        # args    = request.form
        args    = dict(request.form)

    # return render_template(template, **locals())
    return render_template(template, title=template_title, args=args)


# TODO 임시주석처리
# TODO 임시주석처리
# TODO 임시주석처리
# TODO 임시주석처리
# 스크랩핑(Flask가 실행된 후 import를 하도록하자)
# from app.business.stock_symbol_scraping import stock_symbol_load_all 
# stock_symbol_load_all()

if __name__ == "__main__":
    app.debug = False
    app.run()
    