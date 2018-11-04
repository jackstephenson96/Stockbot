import json
import os
import urllib
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import LocalConfig
##teststockbot iota, btc, Barclays PLC, indonesia
arcade_mode = True
extramessage = "https://open.spotify.com/user/jackstephenson96/playlist/6hpWWE9bctQONTLYDxibE2"
##INPUT: message string
##OUTPUT: none
##POSTS message to groupme
def thaPostMan(msg):
	url  = 'https://api.groupme.com/v3/bots/post'

	data = {
		'bot_id' : os.getenv('GROUPME_BOT_ID'),
		'text'   : msg,
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

##INPUT: none
##OUTPUT: List of cryptocurrency JSON objects
## gets list of cryptocurrencies id's, names, and symbols (for NLP)
## caching currently not supported in traditional manner by heroku, but since
## new cryptocurrencies are added every day, doesnt matter
def allTheCryptoStuff():
	# CACHE_FNAME = "cryptos.json"
	# try:
	# 	cache_file = open(CACHE_FNAME,'r')
	# 	cache_contents = cache_file.read()
	# 	cache_file.close()
	# 	CACHE_LIST = json.loads(cache_contents)
	# except:
	CACHE_LIST = []
	url = "https://api.coinmarketcap.com/v1/ticker/?limit=100"
	r = requests.get(url)
	for curr in r.json():
		outty = {"id": curr["id"], "symbol": curr["symbol"], "name": curr["name"]}
		CACHE_LIST.append(outty)
		outty = {}
	# dumped_json_cache = json.dumps(CACHE_LIST)
	# fw = open(CACHE_FNAME,"w")	# fw.write(dumped_json_cache)
	# fw.close()
	## delete cache
	# f = CACHE_FNAME
	# use_by = time.time() - 1 * 60
	# print(os.path.getatime(f))
	# if os.path.getatime(f) < use_by:
	# 	os.remove(f)
	# 	count += 1
	# 	print("Deleted Cache")
	return CACHE_LIST

##INPUT: cryptocurrency string
##OUTPUT: none
## checks if input is a cryptocurrency
def detectiveCrypto(inp):
	inp = inp
	g = allTheCryptoStuff()
	for curr in g:
		if inp in curr.values():
			return (curr["symbol"], curr["name"])
		elif (inp[0].upper() + inp[1:]) in curr.values():
			return (curr["symbol"], curr["name"])
		elif inp.upper() in curr.values():
			return (curr["symbol"], curr["name"])
		elif inp.lower() in curr.values():
			return (curr["symbol"], curr["name"])
		
# print(detectiveCrypto('iota'))

##INPUT: cryptocurrency string
##OUTPUT: cryptocurrency dictionary
## gets cryptocurrency info from coinmarketcap API
def captainCrypto(cryptoName):
	desc = {}
	try:
		name = detectiveCrypto(cryptoName)[1]
		url = "https://api.coinmarketcap.com/v1/ticker/"
		r = requests.get(url + name)
		out = r.json()[0]
		symbol = detectiveCrypto(cryptoName)[0]
		price = out['price_usd']
		desc["pctChg1hr"] = out["percent_change_1h"] + "%"
		desc["pctChg24hr"] = out["percent_change_24h"] + "%"
		desc["pctChg7d"] = out["percent_change_7d"] + "%"
		output = ("currency: " + symbol + "\n" + "price: $" + str(price) + "\n" 
		+ "change in...\n1hr: " + desc["pctChg1hr"] + "\n" + "24hr: " 
		+ desc["pctChg24hr"] + "\n" + "7d: " + desc["pctChg7d"] + "\n")
		return (output, 200)
	except:
		return ("error", 400)
# print(captainCrypto('iota'))

##INPUT: stock name string
##OUTPUT: stock symbol string
## returns ticker symbol when given the name of a stock
def theTickler(stockName):
	stockName = stockName
	url = 'http://autoc.finance.yahoo.com/autoc?'
	# query = "query=" + stockName
	# region = "&region=US"
	# lang = "&lang=en-US"
	# r = requests.get(url + query + region + lang)
	# try:
	# 	symbol = r.json()["ResultSet"]["Result"][0]["symbol"]
	# except:
	# 	symbol = "invalid"
	# return symbol

	params = {"query": stockName, "region": "US", "lang": "en-US"}
	r = requests.get(url, params=params)
	try:
		symbol = r.json()["ResultSet"]["Result"][0]["symbol"]
	except:
		symbol = "invalid"
	return symbol

##INPUT: country string
##OUTPUT: return country code string 
## converts countries to their currency codes, helper for foreigners
def traveler(country):
	url = "https://restcountries.eu/rest/v2/name/"
	Euros = ["Euro", "euro", "EURO", "EUR", "eur"]
	if country in Euros:
		return "EUR"
	country = country
	r = requests.get(url + country)
	response = r.json()
	try:
		return (str(response[0]['currencies'][0]['code']))
	except:
		pass
# print(traveler("japan"))

##INPUT: stock name string
##OUTPUT: stock info dict
## gets stock info from alphavantage api
def misterRegularStock(stockName):
	## for testing of script outside of heroku local env
	# apikey = LocalConfig.AlphaKey
	
	apikey = str(os.getenv('ALPHA_KEY'))
	desc = {}
	name = theTickler(stockName)
	function = 'TIME_SERIES_INTRADAY'
	# symbol = "symbol=" + str(name) + "&"
	# interval = "&interval=1min"
	url = 'https://www.alphavantage.co/query?'
	## 
	params = {"function": function, "symbol": name, "interval": "1min", "apikey": apikey}
	r = requests.get(url, params=params)
	keys = []
	response = r.json()
	try:
		for key in response['Time Series (1min)'].keys():
			keys.append(key)
		firstkey = keys[0]
		lastkey = keys[-1]
		info = {}
		stuff = response['Time Series (1min)'][firstkey]
		# print(response['Time Series (1min)'][lastkey])
		# info["open"] = stuff["1. open"]
		# info["high"] = stuff["2. high"]
		# info["low"] = stuff["3. low"]
		info["close"] = stuff["4. close"]
		# info["volume"] = stuff["5. volume"]
		# output = ("stock: " + name + "\n" + ": $" + str(info["open"]) + "\n" 
		# + "high: $" + str(info["high"]) + "\n" + "low: $" + str(info["low"]) + "\n" 
		# + "close: $" + str(info["close"]) + "\n" + "volume: " + str(info["volume"] + 
		# "\n"))
		output = ("stock: " + name + "\n" + "price: $" + str(info["close"])
		 + "\n" )
		 # + "volume: " + str(info["volume"] + "\n"))
		return (output, 200)
	except:
		return ("error", 400)

# print(misterRegularStock("googl"))

##INPUT: currency code string
##OUTPUT: currency info
## gets foreign currency exchg rate
def foreigners(inp):
	## for testing V outside of my env
	# apikey = LocalConfig.AlphaKey
	apikey = str(os.getenv('ALPHA_KEY'))
	desc = {}
	# name = theTickler(inp)
	function = 'CURRENCY_EXCHANGE_RATE'
	from_currency = 'USD'
	to_currency = inp
	url = 'https://www.alphavantage.co/query?'
	## 
	params = {"function": function, "from_currency": from_currency, "to_currency": inp, "apikey": apikey}
	r = requests.get(url, params=params)
	keys = []
	response = r.json()
	try:
		for key in response['Realtime Currency Exchange Rate'].keys():
			keys.append(key)
		firstkey = keys[0]
		info = {}
		stuff = response['Realtime Currency Exchange Rate']
		info["exchg. rate"] = stuff["5. Exchange Rate"]
		# info["from_currency"] = stuff["2. From_Currency Name"]
		# info["to_currency"] = stuff["4. To_Currency Name"]
		info["from_currency"] = stuff["1. From_Currency Code"]
		info["to_currency"] = stuff["3. To_Currency Code"]

		output = ("1 " + info['from_currency'] + " = " + info["exchg. rate"] 
		+ " " + info["to_currency"])
	
		return (output, 200)
	except:
		return ("error", 400)

##INPUT: string 
##OUTPUT: decides what to do with it, returns either
	## cryptocurrency, stock, foreign currency
## reggie takes each word passed in in app.webhook() and checks first if its a cryptocurrency,
## then if its a stock, and outputs the appropriate output
def reggie_the_reader(word, arcade_mode=False):
	# keywords = ["price", "?", "what is", "what's", "whats", "stock"]
	password = False 
	if captainCrypto(word)[1] == 200:
		return captainCrypto(word)[0]
		print('crpyto')
	elif misterRegularStock(theTickler(word))[1] == 200:
		return misterRegularStock(theTickler(word))[0]
		print('stock')
	elif foreigners(word)[1] == 200:
		return foreigners(word)[0]
		print('currency')
	elif foreigners(traveler(word))[1] == 200:
		return foreigners(traveler(word))[0]
		print('currency2')

	##added for shits
	if arcade_mode == True:
		if word in ["mrepicpassword"]:
			password = True
			return "What does P.C. say today?"
		elif word =="bokbok":
			password = False
			return extramessage
			
	else:
		return 400
	






