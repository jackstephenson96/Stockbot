## Stockbot
Groupme bot to listen for and return info about stocks, currencies, and cryptos

## Goals: 
My goals for this project were simple: create a groupme chatbot to report
cryptocurrency information from within a specific investment groupme. 

## Try it out!
To try out the bot, request to join the "Testing123" https://groupme.com/join_group/36575866/eIVyt3 Groupme and start querying the bot. Simply type “teststockbot” (case doesn’t matter) and then the name of the company, ticker symbol, country, or cryptocurrency you want information on. Since my version of heroku isn’t paid, I only have one dyno to work with, meaning the first call after a “sleep period” will take roughly 30 seconds. If you want to make multiple queries, you can add commas and stockbot will parse them and respond in order.

If you want to run my code locally, just run the testrun.py file and enter your query in the console, it will simulate what goes on in the groupme. Note that the apikey used in the foo.py is stored as a heroku config variable (so is the GROUPME_BOT_ID). However, the alphavantage api is free and it is very simple to retrieve an API key here. If one were to make changes to the actual groupme stockbot, the following steps must be followed:
-	Create a virtual environment on your machine and install the dependencies in requirements.txt
-	Download the heroku CLI
-	Sign in to heroku account, a url will be provided in console.
-	Git add, commit, and push app.py, foo.py (can be named anything), requirements.txt, runtime.txt, and Procfile (these tell heroku how to compile the application slug) to the url.
-	Viola! The bot is up and running

## Some screenshots of the bot in action:
<img src="https://github.com/jackstephenson96/stockbot/blob/master/static/assorted.png" alt="alt text" width="250" height="250">
<img src="https://github.com/jackstephenson96/stockbot/blob/master/static/currencies.png" alt="alt text" width="250" height="250">
