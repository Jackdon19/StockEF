class Position: 
	
	
	def __init__(self, stock, date, buyprice, quan):
		self.stock = stock
		self.date  = date
		self.buyprice = buyprice
		self.quan = quan

	def getValue(self):
		print (self.stock)