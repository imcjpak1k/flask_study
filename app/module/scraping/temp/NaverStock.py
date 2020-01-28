# 종목별조회 "https://finance.naver.com/item/sise_day.nhn?code=005930&page=10".format(code, page)
# 종목별조회 "https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}".format(code, page)
# KOSPI200	"https://finance.naver.com/sise/sise_index_day.nhn?code={code}&page={page}".format(code, page)
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime as dt
import re
import json


def kospi200(tradeInfoDict=None, page=1, startDate=None, endDate=None): 
	""" 
	KOSPI200 지수정보 조회
	"""
	# 초기화
	if tradeInfoDict == None:
		tradeInfoDict = {} 
	# URL정보 
	url	= "https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page={page}".format(page=page);
	#
	with urlopen(url) as stream:
		soup = BeautifulSoup(stream, 'lxml')
		# trTags = soup.select('body > div > table > tr')[1:-3]
		# if len(trTags) == 0 :
		# 	return tradeInfoDict
		for trTag in soup.select('body > div > table > tr')[1:-3]:
			# 	일거래정보 가져오기 
			tdArray	= trTag.select('td');
			# dummy tr skip
			if len(tdArray) != 6 :
				continue 
			# _date	= tdArray[0].text
			date_val	= re.sub('\.', '', tdArray[0].text)
			#기간체크
			if startDate != None and endDate != None and not(startDate <= date_val <= endDate):
				return tradeInfoDict
			# 중복체크(마지막이라고 인식함)
			if tradeInfoDict.get(date_val) != None or len(date_val.strip()) == 0:
				# print('중복...마지막')
				return tradeInfoDict
			# 거래정보 Dict저장
			# _dateArray = date_val.split('.')
			tradeInfoDict[date_val] 	= {
				# "날짜"		: _date,
				"날짜"		: dt.date(int(date_val[:4]), int(date_val[4:6]), int(date_val[6:])),
				"체결가"		: float(re.sub(',', 	'', tdArray[1].text)),
				"전일비"		: float(re.sub(',', 	'', tdArray[2].text)),
				"등락률"		: float(re.sub('\,|\%',	'', tdArray[3].text)),
				"거래량"		: int(	re.sub(',',		'', tdArray[4].text)),
				"거래대금" 	: int(	re.sub(',',		'', tdArray[5].text))
			}
			# end of for
		page += 1
		return kospi200(tradeInfoDict, stock, code, page)
		# end of with openurl	
	return tradeInfoDict

def localStockInfo(tradeInfoDict=None, code=None, page=1, startDate=None, endDate=None): 
	"""
	국내주식 종목별 거래정보 가져오기 
	"""
	# 유효성 검사
	if code == None or len(code.strip()) == 0:
		raise Exception("코드(code)정보를 입력하여 주십시오.") 
	# 초기화
	if tradeInfoDict == None:
		tradeInfoDict = {} 
	# url	= stock_info.get("URL").format(code=code, page=page);
	url	= "https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}".format(code=code, page=page);
	print(url)
	with urlopen(url) as stream:
		soup = BeautifulSoup(stream, 'lxml')
		for trTag in soup.select('body > table > tr')[1:-3] :
			# 	일거래정보 가져오기 
			tdArray	= trTag.select('td')
			if len(tdArray) != 7 :
				continue 
			# print(tdArray[0].text)
			# date_val	= tdArray[0].text
			date_val	= re.sub('\.', '', tdArray[0].text)
			#기간체크
			if startDate != None and endDate != None and not(startDate <= date_val <= endDate):
				return tradeInfoDict
			# 중복체크(마지막이라고 인식함)
			if tradeInfoDict.get(date_val) != None or len(date_val.strip()) == 0:
				return tradeInfoDict 
			# 거래정보 Dict저장
			# _dateArray = date_val.split('.')
			tradeInfoDict[date_val] 	= {
				# "날짜"		: _date,
				"날짜"		: dt.date(int(date_val[:4]), int(date_val[4:6]), int(date_val[6:])),
				"종가"		: int(re.sub(',', 		'', tdArray[1].text)),
				"전일비"		: float(re.sub(',', 	'', tdArray[2].text)),
				"시가"		: int(re.sub(',', 		'', tdArray[3].text)),
				"고가"		: float(re.sub(',', 	'', tdArray[4].text)),
				"저가"		: int(	re.sub(',',		'', tdArray[5].text)),
				"거래량" 	: int(	re.sub(',',		'', tdArray[6].text))
			}
			#end of for
		page += 1
		return localStockInfo(tradeInfoDict, code, page)
		# end of with openurl	
	return tradeInfoDict
		

def overseasStockInfo(tradeInfoDict=None, code=None, page=1, startDate=None, endDate=None): 
	"""
	해외주식정보 가져오기
	"""
	print('함수호출...')
	# 유효성 검사
	if code == None or len(code.strip()) == 0:
		raise Exception("코드(code)정보를 입력하여 주십시오.") 
	# 초기화
	if tradeInfoDict == None:
		tradeInfoDict = {} 
	# url	= stock_info.get("URL").format(code=code, page=page);
	url	= "https://finance.naver.com/world/worldDayListJson.nhn?symbol={code}&fdtc=0&page={page}".format(code=code, page=page);
	print(url)
	with urlopen(url) as stream:
		jsonArray = json.load(stream)
		# print(jsonArray)
		# 결과값이 없으면 진행하지 않음 
		if len(jsonArray) == 0:
			return tradeInfoDict
		for item in jsonArray :
			xymd	= item.get('xymd')
			#기간체크
			if startDate != None and endDate != None and not(startDate <= xymd <= endDate):
				return tradeInfoDict
			# 중복체크(마지막이라고 인식함)
			if tradeInfoDict.get(xymd) != None or len(xymd.strip()) == 0:
				return tradeInfoDict 
			tradeInfoDict[xymd] 	= {
				# "날짜"		: _date,
				"날짜"		: dt.date(int(xymd[:4]), int(xymd[4:6]), int(xymd[6:])),
				"종가"		: item.get('clos'),
				"전일비"		: item.get('diff'),
				"시가"		: item.get('open'),
				"고가"		: item.get('high'),
				"저가"		: item.get('low'),
				"거래량" 	: item.get('gvol')
			}
			# end of for
		page += 1
		return overseasStockInfo(tradeInfoDict, code, page)
		#end of with urlopen
	return tradeInfoDict
	# end of overseasStockInfo()

print(help(localStockInfo))
stock_data = localStockInfo(code='005930', page=1, startDate="20190715", endDate="20190722")
print(stock_data.keys())

# print(help(overseasStockInfo))
# # stock_data = overseasStockInfo(code='DJI@DJI', page=999)
# stock_data = overseasStockInfo(code='SPI@SPX', page=999)
# print(stock_data)

# stock_data = kospi200(page=559)
# print(stock_data)
