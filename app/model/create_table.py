import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
# from sqlalchemy.orm import relationship
# from sqlalchemy import Table, Column, Integer, ForeignKey
from app.module.sql_alchemy_model import DictModel

app = Flask(__name__)
app.config.from_object('config.Config')
logging.getLogger('sqlalchemy.engine').setLevel(app.config['LOG_LEVEL'])
logging.getLogger('sqlalchemy.pool').setLevel(app.config['LOG_LEVEL'])
logging.getLogger('pool_echo').setLevel(app.config['LOG_LEVEL'])
logging.getLogger('sqlalchemy.orm').setLevel(app.config['LOG_LEVEL'])


bcrypt = Bcrypt(app)
db = SQLAlchemy(app, model_class=DictModel)

# https://pypi.org/project/Flask-SQLAlchemy/
# https://github.com/pallets/flask-sqlalchemy
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/
# https://docs.sqlalchemy.org/en/13/dialects/mysql.html

# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#one-to-many
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class User(db.Model):
    __tablename__   = 'user'
    __table_args__  = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    passwd = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    reg_dtm = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, email=None, passwd=None, name=None, reg_dtm=None):
        self.email = email
        self.passwd = bcrypt.generate_password_hash(passwd)
        self.name = name
        self.reg_dtm = reg_dtm

        if not self.reg_dtm:
            self.reg_dtm = datetime.now()

    def __repr__(self):
        return f'<User id={self.id}, email={self.email}, passwd={self.passwd}, name={self.name}, reg_dtm={self.reg_dtm}>'

#  cascade='all,delete'
class Company(db.Model):
    __tablename__   = 'company'
    __table_args__  = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    stock_code = db.Column(db.String(20), unique=True, nullable=True)
    stock_price = db.relationship('StockPrice', back_populates='company')

    def __init__(self, name=None, stock_code=None):
        self.name = name
        self.stock_code = stock_code

    def __repr__(self):
        return f'<Company id={self.id} name={self.name}, stock_code={self.stock_code}>'


class StockPrice(db.Model):
    __tablename__ = 'stock_price'
    __table_args__  = (
        db.UniqueConstraint('company_id', 'trade_date', name='unique_StockPrice_company_id_trade_date'),
        {'mysql_collate': 'utf8_general_ci'},
        #    ForeignKeyConstraint(['id'], ['remote_table.id']),
        #     UniqueConstraint('foo'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    trade_date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Numeric(15,5))
    closing_price = db.Column(db.Numeric(15,5))
    high = db.Column(db.Numeric(15,5))
    low = db.Column(db.Numeric(15,5))
    diff = db.Column(db.Numeric(15,5))
    volumn = db.Column(db.Numeric(15,5))
    reg_dtm = db.Column(db.DateTime)
    company = db.relationship('Company', back_populates='stock_price')

    def __init__(self, company_id=None, trade_date=None, open_price=None, closing_price=None, high=None, low=None, diff=None, volumn=None, reg_dtm=None):
        self.company_id = company_id
        self.trade_date = trade_date
        self.open_price = open_price
        self.closing_price = closing_price
        self.high = high
        self.low = low
        self.diff = diff
        self.volumn = volumn
        self.reg_dtm = reg_dtm
        
        if not self.reg_dtm:
            self.reg_dtm = datetime.now()

    def __repr__(self):
        return f'<StockPrice company_id={self.company_id}, trade_data={self.trade_date}, closing_price={self.closing_price}>'
