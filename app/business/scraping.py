import logging
from app.module.scraping import naver_stock as stock
# from app.model import stock_symbol_info
# from app.model import stock_symbol_trade_info
from app.module import date_util
from app.module.scraping import naver_stock as stock
from flaskr import db
from app.model.models import Company
from app.model.models import StockPrice
from sqlalchemy.sql import func


logger = logging.getLogger(__name__)

# def stock_symbol_load_all():
#     """
#     데이터베이스에 저장된 모든 주식종목 거래정보 LOAD(Scraping)
#     """
#     stock_symbol_cls        = stock_symbol_info.StockSymbolInfo()

#     # 주식종목 전체조회(그리드처리가 있으므로)
#     stock_symbol_list   = stock_symbol_cls.select_stock_symbol_list()
    
#     if stock_symbol_list == None or len(stock_symbol_list) == 0:
#         return

#     # 종목별 처리
#     for data in stock_symbol_list:
#         stock_symbol_load(code=data.get('symbol_code'))



def daily_stock_price(param, endDate='19900101'):
    """
    일별주식사세정보를 LOAD 후 DB적재

    쿼리참조 
        - Group_by, join, filter_by, Subqueries등....
        - https://docs.sqlalchemy.org/en/13/orm/tutorial.html#returning-lists-and-scalars
            
            stmt = db.session.query(StockPrice.company_id, func.max(StockPrice.trade_date).label('max_trade_dt')).filter_by(company_id=22).group_by(StockPrice.company_id)
            stock_price = stmt.one()


            stmt = db.session.query(StockPrice.company_id, func.max(StockPrice.trade_date).label('max_trade_dt')).filter_by(company_id=22).group_by(StockPrice.company_id).subquery()

            q = session.query(User).\
                join(User.orders).\
                join(Order.items).\
                join(Item.keywords)
            q = session.query(User).join(Address)
            q = session.query(User).join(addresses_table)

                    a_alias = aliased(Address)

                q = session.query(User).\
                        join(User.addresses).\
                        join(a_alias, User.addresses).\
                        filter(Address.email_address=='ed@foo.com').\
                        filter(a_alias.email_address=='ed@bar.com')
            
            Where above, the generated SQL would be similar to::

                SELECT user.* FROM user
                    JOIN address ON user.id = address.user_id
                    JOIN address AS address_1 ON user.id=address_1.user_id
                    WHERE address.email_address = :email_address_1
                    AND address_1.email_address = :email_address_2

            q = session.query(User).join(Address, User.id==Address.user_id)

            address_subq = session.query(Address).\
                        filter(Address.email_address == 'ed@foo.com').\
                        subquery()

            q = session.query(User).join(address_subq, User.addresses)

            Producing SQL similar to::

            SELECT user.* FROM user
            JOIN (
                SELECT address.id AS id,
                        address.user_id AS user_id,
                        address.email_address AS email_address
                FROM address
                WHERE address.email_address = :email_address_1
            ) AS anon_1 ON user.id = anon_1.user_id


            q = session.query(User).\
                            join(address_subq, User.id==address_subq.c.user_id)

            q = session.query(Address).select_from(User).\
                            join(User.addresses).\
                            filter(User.name == 'ed')
    """
    # 최근 주가정보조회 (날짜)

    # 마지막거래일자 가져오기
    stmt = db.session.query(StockPrice.company_id, func.max(StockPrice.trade_date).label('trade_date')) \
                .filter_by(company_id=param['company_id'])  \
                .group_by(StockPrice.company_id)            \
                .subquery()
    
    # 마지막거래일자의 거래정보 조회(1건)
    query = db.session.query(StockPrice)    \
                .join(stmt, StockPrice.company_id == stmt.c.company_id) \
                .filter(StockPrice.trade_date == stmt.c.trade_date)
                
    last_deal_data  = query.one_or_none()
    
    base_dt = None
    if last_deal_data : 
        base_dt = last_deal_data.get_trade_date_str()
        StockPrice.query   \
            .filter_by(company_id=last_deal_data.company_id) \
            .filter_by(trade_date=last_deal_data.trade_date) \
            .delete()

    # 일별주가정보 조회호출
    daily_tran_dict    = stock.daily_stock_price(code=param['code'], base_dt=base_dt)

    if not daily_tran_dict or len(daily_tran_dict) == 0 : return

    # session 일별주가 추가
    for daily_item in daily_tran_dict.values():
        db.session.add(
            StockPrice(
                param['company_id'], 
                date_util.strfmt_date(daily_item['trade_date']),
                daily_item['open_price'],
                daily_item['closing_price'],
                daily_item['high'],
                daily_item['low'],
                daily_item['diff'],
                daily_item['volumn'],
            )
        )
    # end of for
    
    # 데이터베이스 데이터반영(commit이전상태)
    db.session.flush()
