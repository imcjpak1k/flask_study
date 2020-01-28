import logging
from app.model import stock_symbol_info
from app.model import stock_symbol_trade_info
from app.module import date_util
from app.module.scraping import naver_stock as stock

logger = logging.getLogger(__name__)

def stock_symbol_load_all():
    """
    데이터베이스에 저장된 모든 주식종목 거래정보 LOAD(Scraping)
    """
    stock_symbol_cls        = stock_symbol_info.StockSymbolInfo()

    # 주식종목 전체조회(그리드처리가 있으므로)
    stock_symbol_list   = stock_symbol_cls.select_stock_symbol_list()
    
    if stock_symbol_list == None or len(stock_symbol_list) == 0:
        return

    # 종목별 처리
    for data in stock_symbol_list:
        stock_symbol_load(code=data.get('symbol_code'))


def stock_symbol_load(code=None, endDate='19900101'):
    """
    단건의 주식종목 거래정보 LOAD(Scraping)
    """
    # 객체생성
    # cur_date                = date_util.current_date_fmt()
    stock_symbol_trade_cls  = stock_symbol_trade_info.StockSymbolTradeInfo()
    stock_symbol_trade_cls.autocommit(True)

    # 주식종목별 최종거래내역 조회(DB)
    # 주식종목별 최종거래내역 조회(DB)
    last_data   = stock_symbol_trade_cls.search_last({'symbol_code':code})
    # print("<< last_data >>")
    # print(last_data)

    reg_date    = None
    trade_date  = None
    if last_data != None:
        endDate     = last_data.get('reg_dt')
        reg_date    = last_data.get('reg_dt')
        trade_date  = last_data.get('trade_date')

    # 최종데이터 삭제처리(거래일자 >= 등록일자, 당일건의 경우에는 거래중일 수 있음.) 
    # 최종데이터 삭제처리(거래일자 >= 등록일자, 당일건의 경우에는 거래중일 수 있음.)
    if reg_date != None and reg_date >= trade_date:
        stock_symbol_trade_cls.delete(last_data)

    # 주식종목별 거래정보(Scraping) 조회
    stock_dict  = stock.local_stock_info(code=code, endDate=endDate)
    stock_list  = stock_dict.values()
    # logging.debug(stock_dict)
    # logging.debug(stock_dict)

    # 주식종목별 거래정보(Scraping) 등록
    # execute_count   = stock_symbol_trade_cls.insert_array(stock_list)
    execute_count   = stock_symbol_trade_cls.merge_array(stock_list)
    if execute_count != None:
        logger.debug('mergie all : {}'.format(execute_count))

    
    stock_symbol_trade_cls.commit()

    