import requests
import investpy
import mysql.connector
from mysql.connector import errorcode
from datetime import *
from forex_python.converter import CurrencyRates
from pymongo import MongoClient
from pprint import pprint

def getProfitThroughIndex(date, amount, Index):
	df = investpy.get_index_historical_data(index = Index,
                                        country='United States',
                                        from_date = date,
                                        to_date= datetime.today().strftime('%d/%m/%y%y'))
	begin = df.first('1D')['Open'].item()
	end = df.last('1D')['Close'].item()
	quote = end/begin
	return amount*quote-amount

def getstockValue(stock, country):
	df = investpy.get_stock_recent_data(stock=stock, country=country, as_json=False, order='ascending')
	a = df.last('1D')['Close'].item()
	b = df.last('1D')['Currency'].item()
	c = CurrencyRates()
	try:
		rate = c.get_rates(b)['EUR']
		return a*rate
	except: 
		return a
	
def stockdevprop(stock, length, comp):
	if length == 0:
		length = 10
	import requests
	#headers = {
    #'x-rapidapi-host': "financial-modeling-prep.p.rapidapi.com",
   # 'x-rapidapi-key': "f892bf9709mshc8cea0ca4c03cabp15194cjsn151aaec9425d"
   # }
	a = 0
	b = []
	c = 0
	url = "https://financialmodelingprep.com/api/v3/income-statement/{}?apikey=b928eb219e46740680131e2c5735c07a".format(stock)
	response = requests.request("GET", url)
	r = response.json()
	while True:
		try:
			r[a+1]
		except: 
			break
		else: 
			a = a+1
			continue
	if length > a:
		c = a
	else:
		c = length
	for i in range(c):
		b.append((r[i]['date'] , r[i][comp]))
	return b
	

def plotfromlist2(list):
	from datetime import datetime
	import matplotlib.pyplot as plt
	a = []
	b = []
	i = 0
	while i < len(list):
	#	if 'e' in list[i][1]:
	#		c = list[i][1].split('.')
	#		d = c[1].split('e+')
	#		e = int(c[0]+d[0])
	#		f = int(d[1])-len(d[0])
	#		while g < f:
	#			e = e*10
	#			g = g+1
	#		a.append(datetime.strptime(list[i][0],'%Y-%m-%d'))
	#		b.append(e)
	#		print(e)
	#	else:
	#	c = list[i][1].split('.')
		a.append(datetime.strptime(list[i][0],'%Y-%m-%d'))
		b.append(list[i][1])
		i = i+1
	plt.plot(a,b)
	plt.show()
	
def showDev(stock, length, d, type1):
	if type == 'Fin':
		plotfromlist2(stockdevprop(stock,length,comp))
	elif type == 'Ratio':
		plotfromlist2(ratioDev(stock,length,comp))

def showDevShare(stock, length, data, stockInfo, type):
	if type == 'Fin':
		plotfromlist2(divideList(stockdevprop(stock,length,data),getStockData(stock, length, stockInfo)))
	elif type == 'Ratio':
		plotfromlist2(divideList(ratioDev(stock,length,data),getStockData(stock, length, stockInfo)))
		
def stockdevprop1(stock, length, comp):
	if length == 0:
		length = 10
	import requests
	#headers = {
    #'x-rapidapi-host': "financial-modeling-prep.p.rapidapi.com",
    #'x-rapidapi-key': "f892bf9709mshc8cea0ca4c03cabp15194cjsn151aaec9425d"
    #}
	a = 0
	b = []
	c = 0
	url =  "https://financialmodelingprep.com/api/v3/ratios/{}?apikey=b928eb219e46740680131e2c5735c07a".format(stock)
	response = requests.request("GET", url)
	r = response.json()
	while True:
		try:
			r[a+1]
		except: 
			break
		else: 
			a = a+1
			continue
	if length > a:
		c = a
	else:
		c = length
	for i in range(c):
		b.append((r[i]['date'] , r[i][comp]))
	return b	

def getStockData(stock, length, comp):
	import requests
	a = 0
	b = []
	c = 0
	url = "https://financialmodelingprep.com/api/v3/enterprise-values/{}?apikey=5c6e71f40a5b6dd5493ce982c74cda69".format(stock)
	response = requests.request("GET", url)
	r = response.json()
	while True:
		try:
			r[a+1]
		except: 
			break
		else: 
			a = a+1
			continue
	if length > a:
		c = a
	else:
		c = length
	for i in range(c):
		b.append((r[i]['date'] , r[i][comp]))
	return b

def divideList(a, b):
	i = 0
	c = []
	while True:
		try:
			a[i][1]/b[i][1]
		except:
			break
		else:
			c.insert(0, (a[i][0] , a[i][1]/b[i][1]))
			i = i+1
	return c
	
def get_tor_session():

    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session


def inputToMongo(data): 
	client = MongoClient("mongodb://Jackdon:Gabin326@cluster0-shard-00-00.sal4j.mongodb.net:27017,cluster0-shard-00-01.sal4j.mongodb.net:27017,cluster0-shard-00-02.sal4j.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-bz5nyq-shard-0&authSource=admin&retryWrites=true&w=majority")
	db = client.Stocks
	db.finance.insert_many(data)
	
def connectSQL():
	try:
		connection = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='Aktien')
		return connection
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		connection.close()
		print("Connection closed")

