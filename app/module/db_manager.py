# import pymysql
import logging
# import os
# import sys
from flask import g

# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
# sys.path.append(sys.path[0])
# from app.module.decorator.decorators import function_parameter
# import config as cfg 
# function_parameter

# flaskr.py의 flask app객체가져오기
# from flaskr import get_flask_app

class Database():
	# def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='fjfj1305', db='stock', charset='utf8', autocommit=False):
	# 	print(cfg.DevelopmentConfig.DATABASE_HOST)
	# 	print(cfg.DevelopmentConfig.DATABASE_HOST)
	# 	print(cfg.DevelopmentConfig.DATABASE_HOST)
	# 	"""
	# 	데이터베이스의 Connection객체 생성
	# 	"""
	# 	self.__conn	= pymysql.connect(	host		= host,
	# 									port		= port, 
	# 									user		= user,
	# 									passwd		= passwd, 
	# 									db 			= db, 
	# 									charset 	= charset,
	# 									autocommit	= autocommit,
	# 									cursorclass	= pymysql.cursors.DictCursor
	# 									)

	# def __init__(self):
	# 	"""
	# 	데이터베이스의 Connection객체 생성
	# 	"""
	# 	self.__conn	= pymysql.connect(	host		= cfg.DevelopmentConfig.DB_HOST,
	# 									port		= cfg.DevelopmentConfig.DB_PORT, 
	# 									user		= cfg.DevelopmentConfig.DB_USER,
	# 									passwd		= cfg.DevelopmentConfig.DB_PASSWD, 
	# 									db 			= cfg.DevelopmentConfig.DB_NAME, 
	# 									charset 	= cfg.DevelopmentConfig.DB_CHARSET,
	# 									autocommit	= cfg.DevelopmentConfig.DB_AUTOCOMMIT,
	# 									cursorclass	= pymysql.cursors.DictCursor
	# 									)

	# def __init__(self):
	# 	"""
	# 	데이터베이스의 Connection객체 생성
	# 	"""
	# 	self.logger = logging.getLogger(__name__)
	# 	#flaskr.py의 flask app객체가져오기
	# 	from flaskr import get_flask_app
	# 	cfg = get_flask_app().config.get('DATABASE')

	# 	self.__conn	= pymysql.connect(	host		= cfg.get('host'),
	# 									port		= cfg.get('port'), 
	# 									user		= cfg.get('user'),
	# 									passwd		= cfg.get('passwd'), 
	# 									db 			= cfg.get('db'), 
	# 									charset 	= cfg.get('charset'),
	# 									autocommit	= cfg.get('autocommit'),
	# 									cursorclass	= cfg.get('cursorclass'),
	# 									)
	def __init__(self):
		"""
		데이터베이스의 Connection객체 생성
		"""
		self.logger = logging.getLogger(__name__)
		# self.__conn	= g.conn
		
		# from flaskr import db
		self.__conn	= get_dbconn()


	# def __del__(self):
	# 	self.__conn.close()

	@property
	def conn(self):
		return self.__conn
	
	def cursor(self):
		return self.__conn.cursor()
	
	def commit(self):
		self.__conn.commit()

	def rollback(self):
		self.__conn.rollback()

	def autocommit(self, bool):
		self.__conn.autocommit(bool)

	# @function_parameter
	def fetchone(self, sql, *args):
		self.logger.debug("fetchone - sql : {} \n args : {}".format(sql, args))

		with self.cursor() as cursor:	
			cursor.execute(sql, *args)
			return cursor.fetchone()

	def fetchall(self, sql, *args):
		self.logger.debug("fetchall - sql : {} \n args : {}".format(sql, args))

		with self.cursor() as cursor:	
			cursor.execute(sql, *args)
			return cursor.fetchall()

	def fetchpaging(self, *args, sql=None, pageinfo=None):
		"""
		pageinfo 정보로 페이징쿼리 및 전체건수를 조회 후 반환
		
		[반환데이터형식]
		{
			data : [{}.....],
			total_count : 1000
			row_count	: 10
		}
		"""
		self.logger.debug("fetchpaging - pageinfo : {} \n sql : {} \n args : {}".format(pageinfo, sql, args))

		# 전체건수 조회
		count_sql	=	"""
						SELECT COUNT(1) AS total_count
						  FROM (
							  {sql}
						  ) T1
						""".format(sql=sql)
		
		count_data	= self.fetchone(count_sql, *args)

        # LIMIT	
		offset		= 0
		row_count	= 10
		if pageinfo != None:
			offset		= pageinfo.get('start', 0)
			row_count	= pageinfo.get('length', 10)

		# paging sql
		sql = sql + \
			"""
			LIMIT {offset}, {row_count}
			""".format(
					offset=offset, 
					row_count=row_count
			)
        
		# 목록 조회
		list_data	= self.fetchall(sql, *args)

		# ret_data	= {
		# 	'total_count'	: count_data.get('total_count'),
		# 	'row_count'		: row_count,
		# 	'data'			: list_data,
		# }
		# self.logger.debug('>>>>>>>>>>>>>>>>> ret_data <<<<<<<<<<<<<<<<<<<<<')
		# self.logger.debug(ret_data)
		return {
			'total_count'	: count_data.get('total_count'),
			'row_count'		: row_count,
			'data'			: list_data,
		}



	def fetchmany(self, sql, size=None, *args):
		self.logger.debug("fetchmany - sql : {} \n size : {} \n args : {}".format(sql, size, args))

		with self.cursor() as cursor:	
			cursor.execute(sql, args)
			return cursor.fetchmany(size)


	def execute(self, sql, *args):
		self.logger.debug("execute - sql : {} \n args : {}".format(sql, args))
		count = 0
		try:
			with self.cursor() as cursor:
				cursor.execute(sql, *args)
				count += 1
		except Exception as e:
			self.logger.exception(e)
			raise
		finally:
			pass

		return count
	
	def executeall(self, sql, array=None):
		if type(array) != list:
			raise TypeError("Array Type 을 입력하세요")
		
		count = 0
		try:
			is_autocommit = self.__conn.get_autocommit()
			with self.cursor() as cursor:
				for data in array:
					self.logger.debug("executeall \n- sql : {} \n- data : {}".format(sql, data))
					cursor.execute(sql, data)
					count += 1

					if is_autocommit == True and count % 1000 == 0:
						self.logger.debug("executeall commit")
						self.commit()

				if is_autocommit == True:
					self.commit()
		except Exception as e:
			self.logger.exception(e)
			self.rollback()
			raise
		finally:
			self.logger.debug("total count : {}".format(count))
		
		# print(count)
		# print(count)
		# print(count)
		# print(count)
		return count





if __name__ == '__main__':
	sql ="""
		SELECT EMAIL, PWD, NAME
		  FROM USERS T1
		 WHERE 1=1
		"""
		   # AND USE_YN	= %s
	db = Database()
	print(db.fetchone(sql))
	print(db.fetchmany(sql, 10))
	print(db.fetchall(sql))
	# print(db.conn)
	# print(dir(conn))