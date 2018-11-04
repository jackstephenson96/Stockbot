## Final project for SI 206: Stockbot
Groupme bot to listen for and return info about stocks, currencies, and cryptos

## Goals: 
My goals for this project were simple: create a groupme chatbot to report
cryptocurrency information from within a specific investment groupme. 
Not wanting to sit around all day running my script in my computers console, I decided to have the script always running in the cloud via Heroku and Flask. 

## Outcome: 
Luckily, I achieved my goals and more. In addition to cryptocurrency information, I also could add stock and country currency functionality. I got my heroku server to work, and the chatbot works perfectly. Anybody in the groupme can call the bot at any time, without the need for the script to be running on any physical machine.

## Try it out!
To try out the bot, request to join the "Testing123" https://groupme.com/join_group/36575866/eIVyt3 Groupme and start querying the bot. Simply type “teststockbot” (case doesn’t matter) and then the name of the company, ticker symbol, country, or cryptocurrency you want information on. Since my version of heroku isn’t paid, I only have one dyno to work with, meaning the first call after a “sleep period” will take roughly 30 seconds. If you want to make multiple queries, you can add commas and stockbot will parse them and respond in order.

## Some screenshots of the bot in action:
<img src="https://github.com/jackstephenson96/stockbot/blob/master/static/assorted.png" alt="alt text" width="250" height="250">
<img src="https://github.com/jackstephenson96/stockbot/blob/master/static/currencies.png" alt="alt text" width="250" height="250">
