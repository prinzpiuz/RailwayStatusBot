HELP_TEXT = """this is my first attempt to make a bot ...
    there will be some errors kindly excuse.........
    maintained by @prinzpiuz 
    for more news subscribe to my channel @princepiuz   
    for help please enter /help  """
help="""for listings trains between stations use 
      /trains <start> <destination>
      eg: for travelling from aluva to banglore enter 
      /trains awy sbc
"""
import urllib3
import json
import time
import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
def start(bot, update):
     update.message.reply_text(HELP_TEXT)
def trains(bot, update, args):
    if len(args)==2:
        text="trains between  " +args[0]+ " and  " +args[1]+"  updating soon"
        date=datetime.datetime.today().strftime('%d-%m-%Y')
        http = urllib3.PoolManager()
        api="https://api.railwayapi.com/v2/between/source/"+args[0]+"/dest/"+args[1]+"/date/"+date+"/apikey/jjmreclucs/"
        print(api)
        r = http.request('GET', api)
        data = json.loads(r.data.decode('utf-8'))
        update.message.reply_text(text)
  #      print(len(data['trains']))
        for i in range(0,len(data['trains'])):
#            print(data['trains'][i]['to_station'])
 #           print(data['trains'][i]['from_station'])
            update.message.reply_text("""train named  """+data['trains'][i]['name']+" with train number: #"+data['trains'][i]['number']+"""
          from  """+data['trains'][i]['from_station']['name']+
          """ to """+ data['trains'][i]['to_station']['name']+ """ 
          starting at """+data['trains'][i]['src_departure_time']+" and arriving at  "+data['trains'][i]['dest_arrival_time']+"""
         total travel time is:"""+data['trains'][i]['travel_time'])
#            update.message.reply_text(data['trains'][i])
    elif len(args) < 2:
        less="need start and destination"
        update.message.reply_text(less)
        update.message.reply_text(help)
    else:
        great="only need start and destination"
        update.message.reply_text(great)
        update.message.reply_text(help)
   # text="trains between  " +args[0]+ " and  " +args[1]+"  updating soon"
   # update.message.reply_text(text) 
def help(bot, update):
    help="""for listings trains between stations use 
    /trains <start> <destination>
    eg: for travelling from aluva to banglore enter  
    /trains awy sbc """
    update.message.reply_text(help)
def main():
    updater = Updater("566810585:AAHQ2-cKDdZ3YnBCGpQDSEoj1SNxDSsW5as")
    j = updater.job_queue
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trains", trains, pass_args=True))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
