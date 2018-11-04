import foo
botName = "teststockbot"
text = input("Enter your groupme query: ")
def webhook():
	data = {'name': 'Jack', "text": text}
	if data['name'].lower() != botName:
		if botName in data['text'].split(" ")[0].lower():
			# print(data['text'].split(" ")[0].lower())
			datatext = data['text'].replace(data['text'].split(" ")[0], "")
			if "," in datatext:
				for word in datatext.split(","):
					word = word.strip()
					msg = foo.reggie_the_reader(word, foo.arcade_mode)
					if msg != 400:
						print(msg)
					elif msg == 400:
						print("I couldn't find that, try again. For support email: jackstephenson96@gmail.com")

			else:
				word = datatext.strip()

				msg = foo.reggie_the_reader(word, foo.arcade_mode)
				if msg != 400:
					print(msg)
				elif msg == 400:
					print("I couldn't find that, try again. For support email: jackstephenson96@gmail.com")
	return "ok", 200

webhook()