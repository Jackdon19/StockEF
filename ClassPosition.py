'''
from ClassPosition import *
MSFT = Position('MSFT','05/06/2020',162,7, 'Main','BUY')
DIS = Position('DIS','07/05/2020',94,11, 'Main', 'BUY')
AIR = Position('AIR.PA','04/05/2020',54,10, 'Main', 'BUY')
MA = Position('MA','14/04/2020', 249, 3, 'Main', 'BUY')
V = Position('V','14/04/2020',159, 5, 'Main', 'BUY')
AIR1 = Position('AIR.PA','08/04/2020',55,10, 'Main', 'BUY')
BRK = Position('BRK-B','24/03/2020',158,6, 'Main', 'BUY')
AIR2 = Position('AIR.PA','29/06/2020',81.11,20, 'Main', 'SELL')
11Bit = Position('11B','10/06/2020',110,15, 'Main', 'BUY')
11Bit1 = Position('11B','13/08/2020',113,5, 'Main', 'BUY')
TEN = Position('TCEHY','07/07/2020',59,26, 'Main', 'BUY')
TEN1 = Position('TCEHY','13/08/2020',56,12, 'Main', 'BUY')
MSFT1= Position('MSFT','13/08/2020',177,2, 'Main','BUY')
SQU = Position('SQ','13/08/2020',118,6, 'Main','BUY')
b = Portfolio()
b.portfolioList.extend((DIS,AIR,MA,V,MSFT,AIR1,BRK))
investpy.get_index_recent_data(index='S&P 500',
                                    country='United States')
S&P 500
'''
from devlist import *
import requests
import investpy
from datetime import *
from forex_python.converter import CurrencyRates
from pymongo import MongoClient
from pprint import pprint
from databasefile import *
class Position: 

	c = CurrencyRates()
	rate = c.get_rates('USD')['EUR']

	
	
	def __init__(self, stock, date, buyprice, quan, Portfolio, Type):
		self.stock = stock
		self.date  = date
		self.buyprice = buyprice
		self.quan = quan
		#self.price = self.getValue()
		#self.totalValue = self.price * self.quan
		self.totalPrice = self.buyprice * self.quan
		#self.result = self.totalValue - self.totalPrice
		self.Portfolio = Portfolio
		self.Type = Type
		self.storeInSQL()

	def getValue(self):
		#check in database for Value eistence
		#if last changed date > 24 hours get value from databse
		url = "https://financialmodelingprep.com/api/v3/quote-short/{}?apikey=5c6e71f40a5b6dd5493ce982c74cda69".format(self.stock)

		response = requests.request("GET", url)
		r = response.json()
		#inputToMongo(r)
		if '.' in self.stock:
			a = r[0]['price']
		else:	
			a = r[0]['price']*self.rate
		return a
	def storeInSQL(self):
		try:
			connection = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='aktien')
			cursor = connection.cursor()
			insert_query = """Insert INTO trades (Item, Quant, Price, Date, PortfolioName, Type, ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
			recordTuple = (self.stock, self.quan, self.buyprice, datetime.strptime(self.date,'%d/%m/%Y').strftime('%Y-%m-%d'), self.Portfolio, self.Type, None)
			cursor.execute(insert_query, recordTuple)
			connection.commit()
			print("Record inserted successfully into table")
		except mysql.connector.Error as error:
			print("Failed to insert into MySQL table {}".format(error))

		finally:
			if (connection.is_connected()):
				cursor.close()
				connection.close()
				print("MySQL connection is closed")
			
class Portfolio:
	indexCountry = [('S&P 500','United States')]
	today = date.today().strftime("%d/%m/%Y")
	
	def __init__(self):
		self.portfolioList = []
		self.Profit = self.getTotalValue() - self.getBuyPrice()
	def addPosition(self, Position):
		self.portfolioList.append(Position)

	def getTotalValue(self):
		a = 0
		for b in self.portfolioList:
			a = a+b.totalValue
		return a
	
	def getBuyPrice(self):
		a = 0
		for b in self.portfolioList:
			a = a+b.totalPrice
		return a	
	def getProfit(self):
		return self.getTotalValue() - self.getBuyPrice()
		
	def printList(self):
		print(self.portfolioList)
	def getAllValues(self):
		for a in self.portfolioList:
			print ('Total Value of Your ',a.stock, 'is' , a.totalValue)
			
	def compareListToIndex(self, Index):
		#countryIn = ''
		#totalInvestVolume = 0
		totalIndexProfit = 0
		#todayIndexValue = 0
		#compareProfit = []
		#for a in self.indexCountry:
		#	if a[0] == Index:
		#		countryIn = a[1]
		for a in self.portfolioList:
			#prof = getProfitThroughIndex(a.date, a.totalPrice, Index)
			totalIndexProfit = totalIndexProfit + getProfitThroughIndex(a.date, a.totalPrice, Index)
			#totalIndexProfit = totalIndexProfit + prof
			#print ('IndexProfit = ' + str(prof))
			#print ('StockProfit =' + str(a.result))
		
		return self.getProfit() - totalIndexProfit								
	
	
	
		