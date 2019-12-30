import os 
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import threading
from signal import signal, SIGINT
from sys import exit
from imageBuilder import ImageBuilder
#API key here
api_key = '5U7U9846S47BG8CE'

#create our timeseries object 
ts = TimeSeries(key=api_key, output_format='pandas')


symbols = ["INTC", "AMD", "MSFT"]
stocks = [] #list of stock objects




#Stock object, each call to  constructor will make 1 API Call
class Stock:
	def __init__(self, symbol):
		self.symbol = symbol
		self.data, self.meta_data = ts.get_quote_endpoint(symbol = self.symbol)
		self.price = "".join(str(self.data['05. price'])[16:].strip())[:-3]
		self.change = "".join(str(self.data['09. change']))[16:].strip()[:-3]
		if self.change[0] == '-':
			self.color = (255, 0,0)
		else:
			self.color = (0,255,0)
		print(self.symbol)
		print("Create")
		print(self.change)
	def getPrice(self):
		return self.price
	def getChange(self):
		return self.change
	def getColor(self):
		return self.color
	def update(self):
		self.data, self.meta_data = ts.get_quote_endpoint(symbol = self.symbol)
		self.price = "".join(str(self.data['05. price'])[16:].strip())[:-3]
		self.change = "".join(str(self.data['09. change']))[16:].strip()[:-3]
		if self.change[0] == '-':
			self.color = (255, 0,0)
		else:
			self.color = (0,255,0)
		print(self.symbol)
		print("UPDATE")
		print(self.price)
	

def main():
	
	# alpha vantage free api gives us 5 calls per minute, but we may not need that many
	opsPerMin = min(5, len(symbols)) 
	def stockUpdater():
		stockIndex = 0
		
		while True:
			i = 0
			for i in range(opsPerMin):
				if len(stocks) != len(symbols):
					stocks.append(Stock(symbols[stockIndex])) # Making API Call, adding new stock to stocks
				else:
					stocks[stockIndex].update()
				if stockIndex == len(symbols) -1 :
					stockIndex = 0
				else:
					stockIndex +=1
				i +=1
			time.sleep(60)
	

	dataThread = threading.Thread(target = stockUpdater)
	dataThread.daemon = True
	dataThread.start()

	
	
	while True:
		builder = ImageBuilder(1000)

		for stock in stocks:
			builder.addImage(stock.symbol, (0,255,255))
			builder.addImage(stock.price, stock.color)

		os.system("sudo python scrolling-image.py -l 1")



		

		


def handler(signal_recieved, frame):
	print("SIGINT or CTRL-C detected. Exiting")
	exit(0)

if __name__ == '__main__':
	main()

