#Manage Database
from devlist import *
import requests
import investpy
from datetime import *
from forex_python.converter import CurrencyRates
from pymongo import MongoClient
from pprint import pprint

connection = connectSQL()
cursor = connection.cursor()

#def UpdateDatabase():
	
	#Complete Update of the database
	#Get
	#Merges all Transaktions into the Portfolios


def MergeTransaktionintoPosition(): 
#fetch all Portfolios into a list
	portfolioList = []
	insert_query = """Select PortfolioName from trades GROUP BY PortfolioName"""
	cursor.execute(insert_query)
	records = cursor.fetchall()
	i = 0
	for row in records:
		i = i+1
		portfolioList.append(row[0])
#for each portfolio find all existing items 
	for item in portfolioList:
#		itemList = []
		
		insert_query = """Select item from trades where PortfolioName = '{}' GROUP BY item""".format(item)
		cursor.execute(insert_query)
		records = cursor.fetchall()
		i1 = 0
		#for each item/position belonging to that Portfolio do the following
		for row in records:
			print(row[0])
			IDS = readSQLQuery("""select * from trades where PortfolioName = '{}' and item = '{}'""".format(item,row[0]))
#			itemList.append(row[0])
			for row1 in IDS:
				print(row[0])
				#if Item is not in Portfolio now, add it
				Positionname = readSQLQuery("""Select Position, Quant, Buyprice from positionlist where PortfolioName = '{}' and Position = '{}'""".format(item,row[0]))
				if row1[6] == "Yes":
					if Positionname is None:
						insertSQLQuery("""INSERT INTO positionlist ( Position, Quant, Buyprice, TotalValue, SingleValue, PortfolioName ) 
									   SELECT trades.Item, trades.Quant, trades.Price, 0, 0, trades.PortfolioName 
									   FROM trades 
									   WHERE trades.ID = {};""".format(row1[0]))			   
						print ('Position created')
					#if item is already there add new trades to item
					#If it is a buy transaction add stock number to it and avarage the buy costs
					else:
						if row1[5] == "BUY":
							Quant1 = Positionname[0][1]+row1[4]
							AVGPrice= (Positionname[0][2]+row1[3])/2
							print(Quant1)
							print(AVGPrice)
						elif row1[5] == "SELL":
							Quant1 = Positionname[0][1]-row1[4]
							AVGPrice = (Positionname[0][2]+row1[3])/2
							print(Quant1)
							print(AVGPrice)
						insertSQLQuery("""UPDATE positionlist SET Quant = {},Buyprice = {} where PortfolioName = '{}' and Position = '{}'""".format(Quant1,AVGPrice,item,row[0]))
					insertSQLQuery("""UPDATE Trades SET New ='No' Where ID = {}""".format(row1[0]))
				else:
					continue
				
		
def getPortfolioValues():
#get the IDs from all Positions
			IDS = readSQLQuery("""Select ID from positionslist""")
	
#def MergePositonintoPortfolio():

#def getPortfolioValues():
#gets the UpotodateValues of the transaktions
def readSQLQuery(Query):
	insert_query = Query
	cursor = connection.cursor(buffered=True)
	cursor.execute(insert_query)	
	row = cursor.fetchone()
	if row is None:
		return None
	else:
		cursor.execute(insert_query)	
		records = cursor.fetchall()
		return records

def insertSQLQuery(Query):
	insert_query = Query
	cursor.execute(insert_query)
	connection.commit()
	