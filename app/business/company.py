import logging 
from app.module import date_util 
from flaskr import db
from app.model.models import Company

logger = logging.getLogger(__name__)

"""
https://docs.sqlalchemy.org/en/13/changelog/migration_12.html
https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
"""
def select_all(param=None):
    # 전체조회
    stock_list  = Company.query.all()

    return [item.toDict() for item in stock_list]

def select_one(param=None):
    """
    회사정보를 단건조회
    """
    id = param.get('id')

    # 조회
    companys = Company.query.filter_by(id=id).all()
    if len(companys) not in [0,1]:
        raise ValueError('단건조회요청 서비스입니다.(n건 조회)')

    return companys[0].toDict()


def insert(param=None):
    """
    회사정보를 등록

    # 모델생성
    company = Company(name, stock_code)

    # session 등록
    db.session.add(company) 
    """
    name = param.get('name')
    stock_code = param.get('stock_code')
    
    # session에 Company등록
    db.session.add( Company(name, stock_code) ) 
    # 데이터베이스 데이터반영(commit이전상태)
    db.session.flush()

    return Company.query.filter_by(name=name).one().toDict()

def update(param=None):
    """
    회사정보 수정
    """
    id = param.get('id')

    # 조회 후 수정
    company = Company.query.filter_by(id=id).update({
        'name' : param.get('name'),
        'stock_code' : param.get('stock_code'),
    })

    return company.toDict()
    # Company.query.filter_by(name=name).one().toDict()

def delete(param=None):
    """
    회사정보 삭제
    """
    id = param.get('id')

    # # 방법1) 회사정보 조회 후 
    # company = Company.query.filter_by(id=id).one()
    # db.session.delete(company)

    # 방법2) 조회 후 delete호출
    Company.query.filter_by(id=id).delete()
    # 데이터베이스 데이터반영(commit이전상태)
    db.session.flush()

    


