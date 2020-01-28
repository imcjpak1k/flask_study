from flask import Blueprint, request, jsonify
import io
import sys
import logging

logger = logging.getLogger(__name__)
this = Blueprint('company', __name__, url_prefix='/company')

sys.path.append(sys.path[0])
from app.module import request_util
from app.module.decorator.login_required import LoginRequired
from app.module.decorator.request_parameter import RequestParameter
from app.module.scraping import naver_stock as stock
from app.business import company as company_biz


@this.route('/test')
def test():
    return 'stocksymbol - test'


@this.route('/search', methods=['GET', 'POST'])
@LoginRequired
@RequestParameter
def search():
    """
    회사조회
    """
    logger.debug("\n\n<< 회사목록조회 >>")
    json_data   = request.get_json(silent=True, cache=False, force=True)
    
    rs_list  = None
    exception   = None
    try:
        # 조회
        rs_list  = company_biz.select_all(json_data)
    except Exception as e:
        exception   = e
    
    # 그리드데이터 변경
    responseData    = request_util.toDatatablesObject(json_data, rs_list, exception)

    return jsonify(responseData)
    

@this.route('/register', methods=['POST'])
@LoginRequired
@RequestParameter
def insert():
    """
    회사정보 등록
    """
    logger.debug("회사정보 등록")
    json_data   = request.get_json(silent=True, cache=False, force=True)

    id = json_data.get('id')
    name = json_data.get('name')
    stock_code = json_data.get('stock_code')

    if name == None or len(name) == 0:
        raise ValueError('회사명을 입력하세요')
    if stock_code == None or len(stock_code) == 0:
        raise ValueError('종목코드를 입력하세요')
    
    company = None
    if id:
        # 수정
        company = company_biz.update(json_data)
    else:
        # 등록
        company = company_biz.insert(json_data)
        
    return jsonify(company)



@this.route('/delete', methods=['POST'])
@LoginRequired
@RequestParameter
def delete():
    """
    회사정보 삭제
    """
    logger.debug("회사정보 삭제")
    json_data   = request.get_json(silent=True, cache=False, force=True)

    id = json_data.get('id')
    if id == None or len(str(id)) == 0:
        raise ValueError('삭제하고자 하는 Company정보를 입력하여 주십시오.')

    # 등록
    company_biz.delete(json_data)
    return jsonify({})


@this.route('/detail', methods=['POST'])
@LoginRequired
@RequestParameter
def detail():
    """
     회사정보 상세조회
    """
    logger.debug("회사정보 상세조회")
    json_data   = request.get_json(silent=True, cache=False, force=True)

    id = json_data.get('id')

    if id == None or len(str(id)) == 0:
        raise ValueError('조회정보를 입력하여 주십시오.')

    # 등록
    company_data = company_biz.select_one(json_data)

    return jsonify(company_data)

@this.route('/search_stock_items', methods=['POST'])
@LoginRequired
@RequestParameter
def search_stock_symbol_scraping():
    """
     종목목록조회
     - 종목코드
     - 종목명
     - 시장
     - 링크
    """
    
    json_data   = request.get_json()

    search_keyword  = json_data.get('search_keyword') 

    items  = None
    exception   = None
    try:
        items = stock.search_stock_items(search_keyword)
    except Exception as e:
        exception   = e
        
    # 그리드데이터 변경
    responseData    = request_util.toDatatablesObject(json_data, items, exception)
    
    return jsonify(responseData)

