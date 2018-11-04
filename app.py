
from flask import Flask, request
import foo
## source activate stockenv
## name of bot for recognition
## Bot ID stored in heroku config for security
botName = "teststockbot"
## starts a Flask instance
app = Flask(__name__)
## take POST requests from URL
@app.route('/', methods=['POST'])


##SOME PARAMS##



##INPUT: none
##OUTPUT: 200 status if correct, 400 if incorrect
## function that parses bot post and posts back to groupme
def webhook():
	data = request.get_json()
	if data['name'].lower() != botName:
		if botName in data['text'].split(" ")[0].lower():
			datatext = data['text'].replace(data['text'].split(" ")[0], "")
			if "," in datatext:
				for word in datatext.split(","):
					word = word.strip()
					msg = foo.reggie_the_reader(word, foo.arcade_mode)
					if msg != 400:
						foo.thaPostMan(msg)
					elif msg == 400:
						foo.thaPostMan("I couldn't find that, try again. For support email: jackstephenson96@gmail.com")

			else:
				word = datatext.strip()
				msg = foo.reggie_the_reader(word, foo.arcade_mode)
				if msg != 400:
					foo.thaPostMan(msg)
				elif msg == 400:
					foo.thaPostMan("I couldn't find that, try again. For support email: jackstephenson96@gmail.com")
	return "ok", 200
# tells heroku to run
if __name__ == "__main__":
	app.run()


## features to add:
	## stocks: rm high/low, add marketcap, 1y change, P/E ratio, EV/EBITDA ratio