# 종목별조회 "https://finance.naver.com/item/sise_day.nhn?code=005930&page=10".format(code, page)
# 종목별조회 "https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}".format(code, page)
# KOSPI200	"https://finance.naver.com/sise/sise_index_day.nhn?code={code}&page={page}".format(code, page)
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import datetime as dt
import re
import json
import logging

logger = logging.getLogger(__name__)


# def kospi200(tradeInfoDict=None, page=1, startDate=None, endDate=None): 
# 	""" 
# 	KOSPI200 지수정보 조회
# 	"""
# 	# 초기화
# 	if tradeInfoDict == None:
# 		tradeInfoDict = {} 
# 	# URL정보 
# 	url	= "https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page={page}".format(page=page);
# 	#
# 	with urlopen(url) as stream:
# 		soup = BeautifulSoup(stream, 'lxml')
# 		# trTags = soup.select('body > div > table > tr')[1:-3]
# 		# if len(trTags) == 0 :
# 		# 	return tradeInfoDict
# 		for trTag in soup.select('body > div > table > tr')[1:-3]:
# 			# 	일거래정보 가져오기 
# 			tdArray	= trTag.select('td');
# 			# dummy tr skip
# 			if len(tdArray) != 6 :
# 				continue 
# 			# _date	= tdArray[0].text
# 			date_val	= re.sub('\.', '', tdArray[0].text)
# 			#기간체크
# 			if startDate != None and endDate != None and not(startDate <= date_val <= endDate):
# 				return tradeInfoDict
# 			# 중복체크(마지막이라고 인식함)
# 			if tradeInfoDict.get(date_val) != None or len(date_val.strip()) == 0:
# 				# logging.debug('중복...마지막')
# 				return tradeInfoDict
# 			# 거래정보 Dict저장
# 			# _dateArray = date_val.split('.')
# 			tradeInfoDict[date_val] 	= {
# 				# "날짜"		: _date,
# 				"날짜"		: dt.date(int(date_val[:4]), int(date_val[4:6]), int(date_val[6:])),
# 				"체결가"		: float(re.sub(',', 	'', tdArray[1].text)),
# 				"전일비"		: float(re.sub(',', 	'', tdArray[2].text)),
# 				"등락률"		: float(re.sub('\,|\%',	'', tdArray[3].text)),
# 				"거래량"		: int(	re.sub(',',		'', tdArray[4].text)),
# 				"거래대금" 	: int(	re.sub(',',		'', tdArray[5].text))
# 			}
# 			# end of for
# 		page += 1
# 		return kospi200(tradeInfoDict, stock, code, page)
# 		# end of with openurl	
# 	return tradeInfoDict

def search_stock_items(search_keyword=None):
	"""
	주식종목코드 및 주식종목 명 가져오기
	
	조회결과 데이터 예제
		{
		"query" : ["삼성", "삼성"],
		"items" : [
		[   [["005930"],["삼성전자"],["코스피"],["\/item\/main.nhn?code=005930"],["005930"]],
			[["028260"],["삼성물산"],["코스피"],["\/item\/main.nhn?code=028260"],["028260"]],
			[["009150"],["삼성전기"],["코스피"],["\/item\/main.nhn?code=009150"],["009150"]],
			[["005935"],["삼성전자우"],["코스피"],["\/item\/main.nhn?code=005935"],["005935"]],
			[["207940"],["삼성바이오로직스"],["코스피"],["\/item\/main.nhn?code=207940"],["207940"]],
			[["010140"],["삼성중공업"],["코스피"],["\/item\/main.nhn?code=010140"],["010140"]],
			[["068290"],["삼성출판사"],["코스피"],["\/item\/main.nhn?code=068290"],["068290"]],
			[["001360"],["삼성제약"],["코스피"],["\/item\/main.nhn?code=001360"],["001360"]],
			[["006400"],["삼성SDI"],["코스피"],["\/item\/main.nhn?code=006400"],["006400"]],
			[["000810"],["삼성화재"],["코스피"],["\/item\/main.nhn?code=000810"],["000810"]]
		],
		[
			[["AG883"],["삼성MMF법인 1_C"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=KR5105AG8837"],["KR5105AG8837"]],
			[["AP657"],["삼성스마트MMF법인 1_C"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=KR5105AP6574"],["KR5105AP6574"]],
			[["35288"],["삼성KODEX200증권상장지수투자신탁[주식]"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=KR5105352888"],["KR5105352888"]],
			[["19115"],["삼성KODEX레버리지증권상장지수투자신탁[주식-파생형]"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=KR5105191153"],["KR5105191153"]],
			[["B9191"],["삼성KODEX코스닥150레버리지증권상장지수투자신탁[주식-파생형]"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=K55105B91912"],["K55105B91912"]],
			[["A8433"],["삼성KODEX단기채권증권상장지수투자신탁[채권]"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=KR5105A84337"],["KR5105A84337"]],
			[["BW384"],["삼성KODEX200TotalReturn증권상장지수투자신탁[주식]"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=K55105BW3843"],["K55105BW3843"]],
			[["B5274"],["삼성신종MMF 151_C"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=K55105B52740"],["K55105B52740"]],
			[["BR083"],["삼성KODEX종합채권(AA-이상)액티브증권상장지수투자신탁[채권]"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=K55105BR0838"],["K55105BR0838"]],
			[["CG978"],["삼성KODEXTop5PlusTotalReturn증권상장지수투자신탁[주식]"],["국내펀드"],["\/fund\/fundDetail.nhn?fundCd=K55105CG9781"],["K55105CG9781"]]
		],
		[],
		[],
		[],
		[]
		]
		}

	"""
	# print("test")	
	# 유효성 검사
	# if search_keyword == None or len(search_keyword.strip()) == 0:
	# 	raise Exception("코드(code)정보를 입력하여 주십시오.") 
	
	# url encoding은 네이버의 인코딩타입입과 한글인코딩타입을 통일시켜야 한다. utf-8
	url = "https://ac.finance.naver.com/ac?q={q}&q_enc=euc-kr&st=111&frm=stock&r_format=json&r_enc=utf-8&r_unicode=0&t_koreng=1&r_lt=111".format(q=quote(search_keyword, encoding='utf-8'))
	
	logger.debug(url)
	item_list	= []
	with urlopen(url) as stream:
		data = json.load(stream)
		item_list = [
			{
				'code'		: item[0][0],
				'name'		: item[1][0],
				'market'	: item[2][0],
				'link'		: item[3][0],
			} 
			for items in data['items'] for item in items
		] 	# comperhension
		# for items in data['items']:
		# 	for item in items:
		# 		item_list.append({
		# 			'code'		: item[0][0],
		# 			'name'		: item[1][0],
		# 			'market'	: item[2][0],
		# 			'link'		: item[3][0],
		# 		})
	
	return item_list



def daily_stock_price(tradeInfoDict=None, code=None, page=1, base_dt=None): 
	"""
	국내주식 종목별 거래정보 가져오기 
	국내주식 종목코드의 일별주가 데이터를 네이버 금융 싸이트에서 가져온다.
	해당 일별주가 정보는 현재일~기준일 이전까지의 정보를 가져오며, 
	만약 기준일 정보가 없으면 모든 데이터를 가져온다.

	code  	: 종목코드
	base_dt	: 기준일자
	"""
	logger.debug(f'''
	  << 국내주식 종목별 거래정보 가져오기 >>
		종목코드 : {code}
		기준일자 : {base_dt}
		페이지 	 : {page}
	''')

	# 유효성 검사
	if code == None or len(code.strip()) == 0: raise Exception("주식종목코드(code)정보를 입력하여 주십시오.") 

	# 초기화
	if tradeInfoDict == None: tradeInfoDict = {} 

	# url	= stock_info.get("URL").format(code=code, page=page);
	url	= "https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}".format(code=code.strip(), page=page)
	logger.debug(url)
	with urlopen(url) as stream:
		soup = BeautifulSoup(stream, 'lxml')
		for trTag in soup.select('body > table > tr')[1:-3] :
			# 	일거래정보 가져오기 
			tdArray	= trTag.select('td')
			if len(tdArray) != 7 : continue 

			# 날짜 - 기간체크
			# logger.debug(tdArray[0].text)
			date_val	= re.sub(r'\.', '', tdArray[0].text)
			if base_dt != None and date_val < base_dt: return tradeInfoDict

			# 중복체크(마지막이라고 인식함)
			if tradeInfoDict.get(date_val) != None or len(date_val.strip()) == 0: return tradeInfoDict 

			# 거래정보 Dict저장
			# _dateArray = date_val.split('.')
			tradeInfoDict[date_val] 	= { 
				"symbol_code"		: code,
				# "trade_date"		: dt.date(int(date_val[:4]), int(date_val[4:6]), int(date_val[6:])),
				"trade_date"		: date_val,
				"closing_price"		: int(re.sub(',', 		'', tdArray[1].text)),
				"diff"				: float(re.sub(',', 	'', tdArray[2].text)),
				"open_price"		: int(re.sub(',', 		'', tdArray[3].text)),
				"high"				: float(re.sub(',', 	'', tdArray[4].text)),
				"low"				: int(re.sub(',',		'', tdArray[5].text)),
				"volumn" 			: int(re.sub(',',		'', tdArray[6].text))
			}
			#end of for
		page += 1

		return daily_stock_price(tradeInfoDict, code, page, base_dt)
		# end of with openurl	
	return tradeInfoDict
		




def overseasStockInfo(tradeInfoDict=None, code=None, page=1, startDate=None, endDate=None): 
	"""
	해외주식정보 가져오기
	"""
	logger.debug('함수호출...')

	# 유효성 검사
	if code == None or len(code.strip()) == 0:
		raise Exception("코드(code)정보를 입력하여 주십시오.") 
	# 초기화
	if tradeInfoDict == None:
		tradeInfoDict = {} 
	# url	= stock_info.get("URL").format(code=code, page=page);
	url	= "https://finance.naver.com/world/worldDayListJson.nhn?symbol={code}&fdtc=0&page={page}".format(code=code, page=page)
	
	logger.debug(url)
	with urlopen(url) as stream:
		jsonArray = json.load(stream)
		# logger.debug(jsonArray)
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


if __name__ == '__main__':
	logger.debug(help(local_stock_info))
	stock_data = local_stock_info(code='005930', page=1, startDate="20190715", endDate="20190722")
	logger.debug(stock_data.keys())

# logger.debug(help(overseasStockInfo))
# # stock_data = overseasStockInfo(code='DJI@DJI', page=999)
# stock_data = overseasStockInfo(code='SPI@SPX', page=999)
# logger.debug(stock_data)

# stock_data = kospi200(page=559)
# logger.debug(stock_data)
