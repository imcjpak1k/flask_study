import logging
import pymysql
import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from dotty_dict import dotty

class Config():
    # 서버ROOT위치
    BASE_DIR      = os.path.abspath(os.path.dirname(__file__))

    # 참조 : https://flask.palletsprojects.com/en/1.1.x/config/
    DEBUG         = False
    TESTING				= False
    LOG_LEVEL			= logging.DEBUG
    LOG_PATH			= '/logs/test.log'
    SECRET_KEY		= "Stock Info"
    MAX_CONTENT_LENGTH  = 10 * 1024 * 1024

    # -----------------------------------------------------------------------------------------
    # BLUEPRINTS
    # -----------------------------------------------------------------------------------------
    BLUEPRINTS			= [ 
      'app.routes.sample',                    # test
      'app.routes.user',       	              # 사용자정보
      'app.routes.company',                   # 회사정보
      'app.routes.scraping',                  # 스크랩핑
      # 'app.routes.stock_symbol_trade_info',   # 주식거래정보
    ]

    # -----------------------------------------------------------------------------------------
    # MARIA_DATABASE
    # -----------------------------------------------------------------------------------------
    MARIA_DATABASE            = {
      'host'        : '127.0.0.1',
      'port'        : 3306,
      'user'        : 'root',
      'passwd'      : 'fjfj1305',
      'db'          : 'stock_alchemy',
      'charset'     : 'utf8',
      'autocommit'  : False,
    }

    
    # -----------------------------------------------------------------------------------------
    # SQLALCHEMY
    # -----------------------------------------------------------------------------------------
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}'.format(
        user = MARIA_DATABASE['user'],
        passwd = MARIA_DATABASE['passwd'],
        host = MARIA_DATABASE['host'],
        port = MARIA_DATABASE['port'],
        db = MARIA_DATABASE['db'],
    )
    # n개의 데이터 베이스를 접속할때 사용함
    # SQLALCHEMY_BINDSapp.config    = {  
    #     'test2': 'mysql+pymysql://root:root@localhost:3306/test2',
    #     'test1': 'mysql+pymysql://root:root@localhost:3306/test1'
    # }
    SQLALCHEMY_POOL_SIZE            = 5
    # SQLALCHEMY_POOL_TIMEOUT         = 9
    SQLALCHEMY_POOL_RECYCLE         = 3600      # 단위:초, -1:무제한, 3600초(1시간)
    SQLALCHEMY_MAX_OVERFLOW         = 10
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN   = True      # Flask-Alchemry, Request 마지막에 commit처리함.


    # -----------------------------------------------------------------------------------------
    # APScheduler
    # -----------------------------------------------------------------------------------------
    # https://github.com/viniciuschiele/flask-apscheduler/blob/master/examples/advanced.py
    JOBS = [
      # Flask서버가 구동시 2번 호출되면서 job id중복오류발생.. ㅡㅡ;;;
        # {
        #     'id': '332423432',
        #     'func': 'app.module.scheduler.new_file:file_create_test',    # 파일명:함수 인듯...
        #     'args': (1, 2),
        #     'trigger': 'interval',
        #     'seconds': 60
        # }
    ]

    SCHEDULER_JOBSTORES = {
        # 'default': SQLAlchemyJobStore(url='sqlite://')
        'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }

    SCHEDULER_EXECUTORS = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(max_workers=5),
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3,
    }

    SCHEDULER_API_ENABLED = True
    # SCHEDULER_TIMEZONE = 



    # -----------------------------------------------------------------------------------------
    # MyBatis XML 경로
    # -----------------------------------------------------------------------------------------
    # MYBATIS_PATH                    = os.path.join(BASE_DIR, 'app\\model\\mybatis.xml').replace('\\', '/')
    MYBATIS_PATH                    = '/myproject/stock/app/model/mybatis.xml'

    # -----------------------------------------------------------------------------------------
    # dotty
    # RestAPI를 이용한 html관리
    # https://pypi.org/project/dotty-dict/
    # -----------------------------------------------------------------------------------------
    PAGE_LIST     = dotty({
      'login'   : {'template':'login.html',   'title':'로그인'},
      'company'   : {
          'list'      : {'template':'company/list.html',       'title':'회사목록'},
          'register'  : {'template':'company/register.html',   'title':'회사등록'},
          'detail'    : {'template':'company/detail.html',      'title':'회사상세조회'},
        },
      'stock'   : {
          'list'  : {'template':'stock/stock_list.html',  'title':'종목목록'},
          'reg'   : {'template':'stock/stock_reg.html',   'title':'종목등록'},
        },
      # 'stock_list'      : 'stock/stock_list.html',
      'sample'          : {
          'mathjax' : {'template':'sample/mathjax.html',  'title':'mathjax예제1'},
          'mathjax2': {'template':'sample/mathjax.html',  'title':'mathjax예제2'},
      },
    })

class DevelopmentConfig(Config):
	pass