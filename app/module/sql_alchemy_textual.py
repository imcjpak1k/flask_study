import logging
import mybatis_mapper2sql
from flask import g



class SQLAlchemyTextual():
	"""
    SQLAlchemy ORM - Textual SQL 사용한 방법

    # 모델에 정의된 컬럼정보 사용
    stmt =   db.text('select email, name  from user')
    db.session.query(User.email, User.name).from_statement(stmt).all()

    # 모델에 정의된 컬럼정보 사용
    stmt =   db.text('select email, name from user where email = :email')
    stmt = stmt.bindparams(email='imcjpak1k@naver.com')
    db.session.query(User.email, User.name).from_statement(stmt).all()

    # 컬럼정보를 입력한
    stmt =   db.text('select email, name from user where email = :email')
    stmt = stmt.bindparams(email='imcjpak1k@naver.com')
    db.session.query(db.Column('email', db.String(20)), db.Column('name', db.String(20))).from_statement(stmt).all()


    # 컬럼정보 입력 및 바인드변수
    stmt =   db.text('select email, name from user where email = :email')
    stmt = stmt.bindparams(email='imcjpak1k@naver.com')
    db.session.query(db.Column('email', db.String), db.Column('name', db.String)).from_statement(stmt).all()


    아래방법은 컬럼정보를 지정하지 않고 조회가능함..
    stmt =   db.text('select email, name  from user')
    db.session.connection().execute(stmt)

    stmt =   db.text('select email, name  from user')
    db.engine.connect().execute(stmt).fetchall()
	"""
	def __init__(self):
		"""
		데이터베이스의 Connection객체 생성
		"""
		self.logger = logging.getLogger(__name__)

		from flaskr import get_mybatis_mapper
		# from flaskr import get_flask_sqlalchemy
		from app.model import models
		self.__mapper	= get_mybatis_mapper()
		# self.__db		= get_flask_sqlalchemy()
		self.__db		= models.db

	@property
	def mapper(self):
		return self.__mapper

	@property
	def db(self):
		return self.__db

	def get_sql(self, query_id=None):
		self.logger.debug(f"\n<< get_sql : query_id='{query_id}' >>")
		return mybatis_mapper2sql.get_child_statement(self.mapper, child_id=query_id, reindent=True)

	def get_alchemy_textual(self, query_id=None):
		self.logger.debug(f"\n<< get_alchemy_textual : query_id='{query_id}' >>")
		return self.db.text( self.get_sql(query_id) )

	def execute(self, stmt=None):
		self.logger.debug(f"\n<< execute '{stmt}' >>")
		return self.db.session.connection().execute(stmt)

	def fetchone(self, stmt=None):
		return self.execute(stmt).fetchone()

	def fetchall(self, stmt=None):
		return self.execute(stmt).fetchall()

	def fetchmany(self, stmt=None, size=None):
		return self.execute(stmt).fetchmany(size)


# 		with self.cursor() as cursor:	
# 			cursor.execute(sql, *args)
# 			return cursor.fetchone()

# 	def fetchall(self, sql, *args):
# 		self.logger.debug("fetchall - sql : {} \n args : {}".format(sql, args))

# 		with self.cursor() as cursor:	
# 			cursor.execute(sql, *args)
# 			return cursor.fetchall()


	# def __del__(self):
	# 	self.__conn.close()



	
# 	def cursor(self):
# 		return self.__conn.cursor()
	
# 	def commit(self):
# 		self.__conn.commit()

# 	def rollback(self):
# 		self.__conn.rollback()

# 	def autocommit(self, bool):
# 		self.__conn.autocommit(bool)

# 	# @function_parameter
# 	def fetchone(self, sql, *args):
# 		self.logger.debug("fetchone - sql : {} \n args : {}".format(sql, args))

# 		with self.cursor() as cursor:	
# 			cursor.execute(sql, *args)
# 			return cursor.fetchone()

# 	def fetchall(self, sql, *args):
# 		self.logger.debug("fetchall - sql : {} \n args : {}".format(sql, args))

# 		with self.cursor() as cursor:	
# 			cursor.execute(sql, *args)
# 			return cursor.fetchall()

# 	def fetchpaging(self, *args, sql=None, pageinfo=None):
# 		"""
# 		pageinfo 정보로 페이징쿼리 및 전체건수를 조회 후 반환
		
# 		[반환데이터형식]
# 		{
# 			data : [{}.....],
# 			total_count : 1000
# 			row_count	: 10
# 		}
# 		"""
# 		self.logger.debug("fetchpaging - pageinfo : {} \n sql : {} \n args : {}".format(pageinfo, sql, args))

# 		# 전체건수 조회
# 		count_sql	=	"""
# 						SELECT COUNT(1) AS total_count
# 						  FROM (
# 							  {sql}
# 						  ) T1
# 						""".format(sql=sql)
		
# 		count_data	= self.fetchone(count_sql, *args)

#         # LIMIT	
# 		offset		= 0
# 		row_count	= 10
# 		if pageinfo != None:
# 			offset		= pageinfo.get('start', 0)
# 			row_count	= pageinfo.get('length', 10)

# 		# paging sql
# 		sql = sql + \
# 			"""
# 			LIMIT {offset}, {row_count}
# 			""".format(
# 					offset=offset, 
# 					row_count=row_count
# 			)
        
# 		# 목록 조회
# 		list_data	= self.fetchall(sql, *args)

# 		# ret_data	= {
# 		# 	'total_count'	: count_data.get('total_count'),
# 		# 	'row_count'		: row_count,
# 		# 	'data'			: list_data,
# 		# }
# 		# self.logger.debug('>>>>>>>>>>>>>>>>> ret_data <<<<<<<<<<<<<<<<<<<<<')
# 		# self.logger.debug(ret_data)
# 		return {
# 			'total_count'	: count_data.get('total_count'),
# 			'row_count'		: row_count,
# 			'data'			: list_data,
# 		}



# 	def fetchmany(self, sql, size=None, *args):
# 		self.logger.debug("fetchmany - sql : {} \n size : {} \n args : {}".format(sql, size, args))

# 		with self.cursor() as cursor:	
# 			cursor.execute(sql, args)
# 			return cursor.fetchmany(size)


# 	def execute(self, sql, *args):
# 		self.logger.debug("execute - sql : {} \n args : {}".format(sql, args))
# 		count = 0
# 		try:
# 			with self.cursor() as cursor:
# 				cursor.execute(sql, *args)
# 				count += 1
# 		except Exception as e:
# 			self.logger.exception(e)
# 			raise
# 		finally:
# 			pass

# 		return count
	
# 	def executeall(self, sql, array=None):
# 		if type(array) != list:
# 			raise TypeError("Array Type 을 입력하세요")
		
# 		count = 0
# 		try:
# 			is_autocommit = self.__conn.get_autocommit()
# 			with self.cursor() as cursor:
# 				for data in array:
# 					self.logger.debug("executeall \n- sql : {} \n- data : {}".format(sql, data))
# 					cursor.execute(sql, data)
# 					count += 1

# 					if is_autocommit == True and count % 1000 == 0:
# 						self.logger.debug("executeall commit")
# 						self.commit()

# 				if is_autocommit == True:
# 					self.commit()
# 		except Exception as e:
# 			self.logger.exception(e)
# 			self.rollback()
# 			raise
# 		finally:
# 			self.logger.debug("total count : {}".format(count))
		
# 		# print(count)
# 		# print(count)
# 		# print(count)
# 		# print(count)
# 		return count





# if __name__ == '__main__':
# 	sql ="""
# 		SELECT EMAIL, PWD, NAME
# 		  FROM USERS T1
# 		 WHERE 1=1
# 		"""
# 		   # AND USE_YN	= %s
# 	db = Database()
# 	print(db.fetchone(sql))
# 	print(db.fetchmany(sql, 10))
# 	print(db.fetchall(sql))
# 	# print(db.conn)
# 	# print(dir(conn))