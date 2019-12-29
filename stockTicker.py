import os 
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import threading
from signal import signal, SIGINT
from sys import exit

#API key here
api_key = '5U7U9846S47BG8CE'

#create our timeseries object 
ts = TimeSeries(key=api_key, output_format='pandas')


symbols = ["INTC", "AMD", "MSFT"]
stocks = [] #list of stock objects




#Stock object, each call to  constructor will make 1 API Call
class Stock:
	def __init__(self, ticker):
		self.ticker = ticker
		self.data, self.meta_data = ts.get_quote_endpoint(symbol = self.ticker)
		self.price = "".join(str(self.data['05. price'])[16:].strip())[:-3]
		self.change = "".join(str(self.data['09. change']))[16:].strip()[:-3]
		print(self.ticker)
		print("Create")
		print(self.change)
	def getPrice(self):
		return self.price
	def getChange(self):
		return self.change
	def update(self):
		self.data, self.meta_data = ts.get_quote_endpoint(symbol = self.ticker)
		self.price = "".join(str(self.data['05. price'])[16:].strip())[:-3]
		self.change = "".join(str(self.data['09. change']))[16:].strip()[:-3]
		print(self.ticker)
		print("UPDATE")
		print(self.price)
	def printToMatrix(self):
		priceString = "sudo ./scrolling-text-example -y -2 -l 1  -f helvetica.bdf --led-rows 16 --led-cols 64 -s 3  "
		changeString = "sudo ./scrolling-text-example -y -2 -l 1 -f helvetica.bdf --led-rows 16 --led-cols 64 -s 3 "
		tickerString = "sudo ./scrolling-text-example -y -2 -l 1 -f helvetica.bdf --led-rows 16 --led-cols 64 -s 2 -C 0,0,255 "
		if(self.change[0] == "-"):
			priceString += "-C 255,0,0 "
			changeString += "-C 255,0,0 "
		else:
			priceString += "-C 0,255,0 "
			changeString += "-C 0,255,0 "

		tickerString += self.ticker
		tickerString += " "
		tickerString += self.price
		
		changeString += " Daily Change "
		changeString += self.change[1:]
		
		os.system(tickerString)		
		os.system(changeString)

def main():
	
	# alpha vantage free api gives us 5 calls per minute, but we may not need that many
	opsPerMin = min(5, len(symbols)) 
	def stockUpdater():
		stockIndex = 0
		try:
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
		except: KeyboardInterrupt

	dataThread = threading.Thread(target = stockUpdater)
	dataThread.daemon = True
	dataThread.start()
	try:
		while True:
			for stock in stocks:
				stock.printToMatrix()
	except: KeyboardInterrupt
		


def handler(signal_recieved, frame):
	print("SIGINT or CTRL-C detected. Exiting")
	exit(0)

if __name__ == '__main__':
	main()

