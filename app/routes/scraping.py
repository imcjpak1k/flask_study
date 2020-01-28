from flask import Blueprint, request, jsonify
import io
import sys
import logging

logger = logging.getLogger(__name__)
this = Blueprint('scraping', __name__, url_prefix='/scraping')

from app.module import request_util
from app.module.decorator.login_required import LoginRequired
from app.module.decorator.request_parameter import RequestParameter
from app.module.scraping import naver_stock as stock
from app.business import scraping as scriaping_biz


@this.route('/test')
def test():
    return 'scraping - test'


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
    json_data = request.get_json(silent=True, cache=False, force=True)
    search_keyword = json_data.get('search_keyword') 

    items       = None
    exception   = None
    try:
        items = stock.search_stock_items(search_keyword)
    except Exception as e:
        exception   = e
        
    # 그리드데이터 변경
    responseData    = request_util.toDatatablesObject(json_data, items, exception)
    
    return jsonify(responseData)


@this.route('/daily_stock_price', methods=['POST'])
@LoginRequired
@RequestParameter
def daily_stock_price():
    # json data
    json_data       = request.get_json(silent=True, cache=False, force=True)

    # 일별거래정보 LOAD
    scriaping_biz.daily_stock_price(json_data)
    
    return jsonify({})