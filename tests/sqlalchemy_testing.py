import logging
import pymysql
from dotty_dict import dotty


MARIA_DATABASE            = {
  'host'        : '127.0.0.1',
  'port'        : 3306,
  'user'        : 'root',
  'passwd'      : 'fjfj1305',
  'db'          : 'test',
  'charset'     : 'utf8',
  'autocommit'  : False,
  'cursorclass' : pymysql.cursors.DictCursor
}

SQLAlchemy_URL  = 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}'.format(
    user  = MARIA_DATABASE['user'],
    passwd  = MARIA_DATABASE['passwd'],
    host  = MARIA_DATABASE['host'],
    port  = MARIA_DATABASE['port'],
    db  = MARIA_DATABASE['db'],
)

# https://docs.sqlalchemy.org/en/13/core/pooling.html#connection-pool-configuration

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

# pool_size, max_overflow, pool_recycle,  pool_timeout
engine = create_engine(SQLAlchemy_URL, encoding='utf-8', echo=True, pool_size=5, max_overflow=10)

from sqlalchemy.pool import QueuePool
engine = create_engine(SQLAlchemy_URL, encoding='utf-8', 
        echo=True, 
        pool_size=5, 
        max_overflow=10, 
        poolclass=QueuePool)


from sqlalchemy.pool import NullPool
engine = create_engine(SQLAlchemy_URL, encoding='utf-8', 
        echo=True, 
        pool_size=5, 
        max_overflow=10, 
        poolclass=NullPool
        )


# https://docs.sqlalchemy.org/en/13/core/connections.html#using-transactions
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))



# bind=engine
#https://docs.sqlalchemy.org/en/13/core/tutorial.html
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()
# _users 테이블 정의
users = Table('users', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(100)),
                Column('fullname', String(200)),
        )
# _addresses 테이블정의
addresses = Table('addresses', metadata,
                Column('id', Integer, primary_key=True),
                Column('user_id', None, ForeignKey('users.id')),
                Column('email_address', String(200), nullable=False)
        )

# 테이블생성
metadata.create_all(engine)

# 2019-11-09 23:16:32,644 INFO sqlalchemy.engine.base.Engine DESCRIBE `_users`
# 2019-11-09 23:16:32,645 INFO sqlalchemy.engine.base.Engine {}
# 2019-11-09 23:16:32,667 INFO sqlalchemy.engine.base.Engine ROLLBACK
# 2019-11-09 23:16:32,679 INFO sqlalchemy.engine.base.Engine DESCRIBE `_addresses`
# 2019-11-09 23:16:32,680 INFO sqlalchemy.engine.base.Engine {}
# 2019-11-09 23:16:32,695 INFO sqlalchemy.engine.base.Engine ROLLBACK
# 2019-11-09 23:16:32,719 INFO sqlalchemy.engine.base.Engine 
# CREATE TABLE _users (
#         id INTEGER NOT NULL AUTO_INCREMENT,
#         name VARCHAR(100),
#         fullname VARCHAR(200),
#         PRIMARY KEY (id)
# )


# 2019-11-09 23:16:32,722 INFO sqlalchemy.engine.base.Engine {}
# 2019-11-09 23:16:32,758 INFO sqlalchemy.engine.base.Engine COMMIT
# 2019-11-09 23:16:32,760 INFO sqlalchemy.engine.base.Engine 
# CREATE TABLE _addresses (
#         id INTEGER NOT NULL AUTO_INCREMENT,
#         user_id INTEGER,
#         email_address VARCHAR(200) NOT NULL,
#         PRIMARY KEY (id),
#         FOREIGN KEY(user_id) REFERENCES _users (id)
# )


# 2019-11-09 23:16:32,763 INFO sqlalchemy.engine.base.Engine {}
# 2019-11-09 23:16:32,785 INFO sqlalchemy.engine.base.Engine COMMIT
# >>> 

# 1건 등록
ins = users.insert()


ins = users.insert().values(name='jack', fullname='Jack Jones') 
conn = engine.connect()
result = conn.execute(ins)
# 2019-11-09 23:24:34,556 INFO sqlalchemy.engine.base.Engine INSERT INTO _users (name, fullname) VALUES (%(name)s, %(fullname)s) 
# 2019-11-09 23:24:34,556 INFO sqlalchemy.engine.base.Engine {'name': 'jack', 'fullname': 'Jack Jones'}
# 2019-11-09 23:24:34,584 INFO sqlalchemy.engine.base.Engine COMMIT

# n건 등록
values = [
        {'name' :'jack1', 'fullname' : 'Jack Jones1'},
        {'name' :'jack2', 'fullname' : 'Jack Jones2'},

        {'name' :'jack3', 'fullname' : 'Jack Jones3'},
        {'name' :'jack4', 'fullname' : 'Jack Jones4'},
] 
result = conn.execute(users.insert(), values)
# 2019-11-09 23:27:06,300 INFO sqlalchemy.engine.base.Engine INSERT INTO _users (name, fullname) VALUES (%(name)s, %(fullname)s) 
# 2019-11-09 23:27:06,301 INFO sqlalchemy.engine.base.Engine ({'name': 'jack1', 'fullname': 'Jack Jones1'}, {'name': 'jack2', 'fullname': 'Jack Jones2'}, {'name': 'jack3', 'fullname': 'Jack Jones3'}, {'name': 'jack4', 'fullname': 'Jack Jones4'})
# 2019-11-09 23:27:06,322 INFO sqlalchemy.engine.base.Engine COMMIT


values = [
        {'user_id' :1, 'email_address' : 'test@xxx.com'},
        {'user_id' :2, 'email_address' : 'test@xxx.com'},
        {'user_id' :3, 'email_address' : 'test@xxx.com'},
        {'user_id' :4, 'email_address' : 'test@xxx.com'},
        {'user_id' :5, 'email_address' : 'test@xxx.com'},
] 
result = conn.execute(addresses.insert(), values)


# https://docs.sqlalchemy.org/en/13/core/tutorial.html
# 조회
from sqlalchemy.sql import select

# 조회1
# SELECT users.id, users.name, users.fullname 
# FROM users
s = select([users])
result = conn.execute(s)

# 조회-결과확인1
for row in result:
        # print(row)
        print(row['name'])


# 조회-결과확인2
row = result.fetchone()

# 조회-결과확인3
for row in conn.execute(s):
        print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])


if not result.closed:
        result.close()



# 조회2
# SELECT users.name, users.fullname 
# FROM users
s = select([users.c.name, users.c.fullname])
result = conn.execute(s)


# join 조건 없음
# SELECT users.id, users.name, users.fullname, addresses.id, addresses.user_id, addresses.email_address
# FROM users, addresses
for row in conn.execute(select([users, addresses])):
        print(row)


# id join 
s = select([users, addresses]).where(users.c.id == addresses.c.user_id)
for row in conn.execute(s):
        print(row)

# where 
# users.name is null
print(users.c.name == None)
# users.name || users.fullname - 문자
print(users.c.name + users.c.fullname)

# users.id + users.id   - 숫자
print(users.c.id + users.c.id)

# 지원하지 않는 문법은 op에 입력해서 처리함
# users.name tiddlywinks :name_1
print(users.c.name.op('tiddlywinks')('foo'))

# SELECT users.id, users.name, users.fullname, addresses.id, addresses.user_id, addresses.email_address
# FROM users, addresses
# WHERE users.id = addresses.user_id AND users.id > %(id_1)s
# 2019-11-13 23:33:50,190 INFO sqlalchemy.engine.base.Engine {'id_1': 3}
# (4, 'jack3', 'Jack Jones3', 4, 4, 'test@xxx.com')
s = select([users, addresses]).where(and_(users.c.id == addresses.c.user_id, users.c.id > 3))
for row in conn.execute(s):
        print(row)

# SELECT users.id, users.name, users.fullname, addresses.id, addresses.user_id, addresses.email_address
# FROM users, addresses
# WHERE users.id = addresses.user_id 
# AND users.id > %(id_1)s 
# AND users.fullname LIKE %(fullname_1)s
s = select([users, addresses]).where(
                        and_(
                                users.c.id == addresses.c.user_id, 
                                users.c.id > 3,
                                users.c.fullname.like('%Jack%'),
                        )
                )

# SELECT users.fullname, 
#       concat(concat(users.fullname, %(fullname_1)s), addresses.email_address) AS title
# FROM users, addresses
# WHERE users.id = addresses.user_id AND users.name BETWEEN %(name_1)s AND %(name_2)s AND (addresses.email_address LIKE %(email_address_1)s OR addresses.email_address LIKE %(email_address_2)s)
s = select([
                users.c.fullname, 
                (users.c.fullname + ", " + addresses.c.email_address).label('title')
        ]).where(
                and_(
                    users.c.id == addresses.c.user_id,
                    users.c.name.between('m', 'z'),
                    or_(
                       addresses.c.email_address.like('%@aol.com'),
                       addresses.c.email_address.like('%@msn.com')
                    )
                )
        )

# 직접쿼리를 사용하는경우
# SELECT users.fullname || ', ' || addresses.email_address AS title 
#                 FROM users, addresses
#                 WHERE users.id = addresses.user_id
#                 AND users.name BETWEEN %(x)s AND %(y)s
#                 AND (addresses.email_address LIKE %(e1)s
#                 OR addresses.email_address LIKE %(e2)s)
from sqlalchemy.sql import text
s = text(
                """
                SELECT users.fullname || ', ' || addresses.email_address AS title 
                FROM users, addresses 
                WHERE users.id = addresses.user_id 
                AND users.name BETWEEN :x AND :y 
                AND (addresses.email_address LIKE :e1 
                OR addresses.email_address LIKE :e2)
                """.strip()
        )
conn.execute(s, x='m', y='z', e1='%@aol.com', e2='%@msn.com').fetchall()


stmt = text("SELECT id, name FROM users")
stmt = stmt.columns(id=Integer, name=String)
# result = conn.execute(stmt, {"x": "m", "y": "z"}) 
result = conn.execute(stmt) 
for row in result:                                            
        print(row)
# (2, 'jack1')
# (3, 'jack2')
# (4, 'jack3')
# (5, 'jack4')


stmt = text("SELECT id, name FROM users")
stmt = stmt.columns(users.c.id, users.c.name)
result = conn.execute(stmt) 
for row in result:                                            
        print(row)


tmt = text("SELECT users.id, addresses.id, users.id, "
...     "users.name, addresses.email_address AS email "
...     "FROM users JOIN addresses ON users.id=addresses.user_id "
...     "WHERE users.id = 1").columns(
...        users.c.id,
...        addresses.c.id,
...        addresses.c.user_id,
...        users.c.name,
...        addresses.c.email_address
...     )
SQL>>> result = conn.execute(stmt)


# count, group by , order by 
# SELECT addresses.user_id, count(addresses.id) AS num_addresses      
# FROM addresses 
# GROUP BY addresses.user_id 
# ORDER BY addresses.user_id, num_addresses
from sqlalchemy import func
stmt = select([
                addresses.c.user_id,
                func.count(addresses.c.id).label('num_addresses')
        ])      \
        .group_by("user_id")    \
        .order_by("user_id", "num_addresses")

conn.execute(stmt).fetchall()


# SELECT addresses.user_id, count(addresses.id) AS num_addresses 
# FROM addresses GROUP BY addresses.user_id ORDER BY addresses.user_id, num_addresses DESC
from sqlalchemy import func, desc
stmt = select([
        addresses.c.user_id,
        func.count(addresses.c.id).label('num_addresses'),
        ])                      \
        .group_by("user_id")    \
        .order_by("user_id", desc("num_addresses"))

conn.execute(stmt).fetchall()


# table alias
# SELECT users_1.id, users_1.name, users_1.fullname, users_2.id, users_2.name, users_2.fullname
# FROM users AS users_1, users AS users_2
# WHERE users_1.name > users_2.name 
# ORDER BY users_1.name
u1a, u1b = users.alias(), users.alias()
stmt = select([u1a, u1b]).\
        where(u1a.c.name > u1b.c.name).\
        order_by(u1a.c.name)  # using "name" here would be ambiguous

conn.execute(stmt).fetchall()

if not result.closed:
        result.close()



# 서브쿼리
# SELECT users.id, users.name, users.fullname 
# FROM users, addresses AS addresses_1, addresses AS addresses_2
# WHERE users.id = addresses_1.user_id 
# AND users.id = addresses_2.user_id 
# AND addresses_1.email_address = %(email_address_1)s 
# AND addresses_2.email_address = %(email_address_2)s
a1 = addresses.alias()
a2 = addresses.alias()
s = select([users]).\
        where(and_(
            users.c.id == a1.c.user_id,
            users.c.id == a2.c.user_id,
            a1.c.email_address == 'jack@msn.com',
            a2.c.email_address == 'jack@yahoo.com'
        ))
conn.execute(s).fetchall()


# SELECT users.name 
# FROM users, (SELECT users.id AS id, users.name AS name, users.fullname AS fullname
#               FROM users, addresses AS addresses_1, addresses AS addresses_2
#               WHERE users.id = addresses_1.user_id 
#               AND users.id = addresses_2.user_id 
#               AND addresses_1.email_address = %(email_address_1)s 
#               AND addresses_2.email_address = %(email_address_2)s
#               ) AS anon_1
# WHERE users.id = anon_1.id
addresses_subq = s.alias()
s = select([users.c.name]).where(users.c.id == addresses_subq.c.id)
conn.execute(s).fetchall()


# Using Joins -- ANSI SQL로 생성된다...
# ForeginKey를 이용한 join쿼리 생성
print(users.join(addresses))
# users JOIN addresses ON users.id = addresses.user_id

print(users.join(addresses, addresses.c.email_address.like(users.c.name + '%')))
# users JOIN addresses ON addresses.email_address LIKE users.name || :name_1

from sqlalchemy.sql import select
conn = engine.connect()

# uninsql
# SELECT users.fullname 
#  FROM users 
#       INNER JOIN addresses 
#       ON addresses.email_address LIKE concat(users.name, %(name_1)s)
s = select([users.c.fullname]).select_from(
                users.join(addresses, addresses.c.email_address.like(users.c.name + '%'))
        )
print(s)
# conn.execute(s).fetchall()

# SELECT users.fullname 
#  FROM users 
#       JOIN addresses 
#       ON users.id = addresses.user_id
s = select([users.c.fullname]).select_from(users.join(addresses))

# 기존의 오라클쿼리도 사용가능..
# SELECT users.fullname 
# FROM users, addresses
# WHERE users.id = addresses.user_id
print(s.compile(dialect=OracleDialect(use_ansi=False)))

# SELECT users.fullname 
#  FROM users 
#       LEFT OUTER JOIN addresses 
#       ON users.id = addresses.user_id
s = select([users.c.fullname]).select_from(users.outerjoin(addresses))
print(s)


# 기존의 오라클쿼리도 사용가능..
# SELECT users.fullname 
# FROM users, addresses
# WHERE users.id = addresses.user_id(+)
from sqlalchemy.dialects.oracle import dialect as OracleDialect
print(s.compile(dialect=OracleDialect(use_ansi=False)))




# bindparam (바인드변수)
# username 바인드변수
from sqlalchemy.sql import bindparam
# SELECT users.id, users.name, users.fullname 
# FROM users
# WHERE users.name = :username
s = users.select(users.c.name == bindparam('username'))
conn.execute(s, username='jack').fetchall()






# SELECT users.id, users.name, users.fullname, addresses.id, addresses.user_id, addresses.email_address 
# FROM users, addresses
# WHERE users.name LIKE :name || '%' OR addresses.email_address LIKE :name || '@%'
s = select([users, addresses]).where(
        or_(
                users.c.name.like(bindparam('name', type_=String) + text("'%'")),
                addresses.c.email_address.like(bindparam('name', type_=String) + text("'@%'")),
        )
)
conn.execute(s, name='jack').fetchall()


# SELECT users.id, users.name, users.fullname, addresses.id, addresses.user_id, addresses.email_address 
#  FROM users 
#       LEFT OUTER JOIN addresses 
#         ON users.id = addresses.user_id
# WHERE users.name LIKE :name || '%' 
#       OR addresses.email_address LIKE :name || '@%' ORDER BY addresses.id
from sqlalchemy import select, and_, or_, text, String
s = select([users, addresses]).where(
        or_(
                users.c.name.like(bindparam('name', type_=String) + text("'%'")),
                addresses.c.email_address.like(bindparam('name', type_=String) + text("'@%'")),
        )
).select_from(users.outerjoin(addresses)).order_by(addresses.c.id)
conn.execute(s, name='jack').fetchall()


















------------------------------------



from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import pymysql

MARIA_DATABASE            = {
  'host'        : '127.0.0.1',
  'port'        : 3306,
  'user'        : 'root',
  'passwd'      : 'fjfj1305',
  'db'          : 'test',
  'charset'     : 'utf8',
  'autocommit'  : False,
  'cursorclass' : pymysql.cursors.DictCursor
}

SQLAlchemy_URL  = 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}'.format(
    user  = MARIA_DATABASE['user'],
    passwd  = MARIA_DATABASE['passwd'],
    host  = MARIA_DATABASE['host'],
    port  = MARIA_DATABASE['port'],
    db  = MARIA_DATABASE['db'],
)

engine = create_engine(SQLAlchemy_URL, encoding='utf-8', 
        echo=True, 
        pool_size=5, 
        max_overflow=10, 
        poolclass=QueuePool)





from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
 
 
Base = declarative_base()
 
 
class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
 
 
class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    department = relationship(
        Department,
        backref=backref('employees',
            uselist=True,
            cascade='delete,all'
        )
    )

 




 
from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)
# session = sessionmaker()
# session.configure(bind=engine)
Base.metadata.create_all(engine)

