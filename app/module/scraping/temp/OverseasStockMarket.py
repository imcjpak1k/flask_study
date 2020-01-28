# https://finance.naver.com/world/worldDayListJson.nhn?symbol=SPI@SPX&fdtc=0&page=1
# https://finance.naver.com/world/worldDayListJson.nhn?symbol=SPI@SPX&fdtc=0&page=4
from urllib.request import urlopen
import json

def getOverseasStockMarket(dtockMarksetArray=None, symbol='SPI@SPX', page=1):
	# 초기화
	if dtockMarksetArray == None:
		dtockMarksetArray = []
	isContinue	= True
	while isContinue:
		naver_url = "https://finance.naver.com/world/worldDayListJson.nhn?symbol={symbol}&fdtc=0&page={page}".format(symbol=symbol, page=page)
		print(naver_url)
		with urlopen(naver_url) as stream : 
			resJsonData	= json.load(stream)
			for eachData in resJsonData:
				# 중복건이 존재하면 멈춤
				if dtockMarksetArray.count(eachData) != 0:
					isContinue	= False
					break
				# 1건씩 추가
				dtockMarksetArray.append(eachData)
		page += 1
	return dtockMarksetArray



# print(getKospi(page=1))
stockData	= getOverseasStockMarket(page=400)
# print(stockData)
# for key in sorted(stockData) : 
for dalilyData in stockData :  
	print("구분={symb}, 날짜={date}, 마감가={price}".format(symb=dalilyData['symb'] , date=dalilyData.get("xymd"), price=dalilyData.get("clos")))