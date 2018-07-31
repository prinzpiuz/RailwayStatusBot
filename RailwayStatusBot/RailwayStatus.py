stationcode="""                                                                                                                                                                                         
ALLP    Alappuzha
AWY     Aluva
CLT     Calicut
CAN     Cannanore
CKI     Chalakudi
CGY     Changanacherry
ERS     Ernakulam Junction
ERN     Ernakulam Town
KGQ     Kasaragod
KYJ     Kayamkulam
KZK     Kazhakuttam
QLN     Kollam Junction
KTYM    Kottayam
QLD     Koyilandy
KTU     Kuttippuram
PGTN    Palakkad Town
SRR     Shoranur
TVP     Thiruvananthapuram Pettah
TCR     Trichur
TVC     Trivandrum Central
KCVL    Trivandrum Kochuveli
 
 -------------outside kerala--------------
  
Chennai Central (MAS)
Chennai Egmore (MS)
Bangalore Cy Junction (SBC)
Bangalore East (BNCE)
Hyderabad Decan (HYB)
Secunderabad Junction (SC)
Mumbai Central (BCT)
Pune Junction (PUNE)
Madgaon (MAO)
New Delhi (NDLS)
Kolkata (CP)
Srinagar (SNAR)
Kanyakumari (CAPE)
Patna Junction (PNBE) 
 """

HELP_TEXT = """this is my first attempt to make a bot ...
    there will be some errors kindly excuse.........
    maintained by @prinzpiuz 
    for more news subscribe to my channel @princepiuz   
    for help please enter /help 
    source code is available 
    https://github.com/prinzpiuz/RailwayStatusBot
    suggetions and contributions are always welcome
    #FreeAsInFreedom

    """
help="""for listings trains between stations use 
      /trains <start> <destination>
      eg: for travelling from aluva to banglore enter 
      /trains awy sbc
      for listing short station codes 
      /code
      for listing trains on particular date
      /date <start> <dest> <dd> <mm> <yyyy>
      eg: /date awy sbc 15 08 2018
"""
import logging
logging.basicConfig(
    filename="Rail.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )
import configparser
import urllib3
import json
import time
import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
config = configparser.RawConfigParser()
config.read('rail.cfg')
token=config.get('telegram','token')
key=config.get('railwayAPI','key')
logging.info(key)
logging.info(token)
def start(bot, update):
     update.message.reply_text(HELP_TEXT)
def trains(bot, update, args):
    if len(args)==2:
        text="trains between  " +args[0]+ " and  " +args[1]+"  are............."
        date=datetime.datetime.today().strftime('%d-%m-%Y')
        http = urllib3.PoolManager()
        api="https://api.railwayapi.com/v2/between/source/"+args[0]+"/dest/"+args[1]+"/date/"+date+"/apikey/"+key+"/"
        logging.info(api)
        r = http.request('GET', api)
        data = json.loads(r.data.decode('utf-8'))
        if data['response_code'] != 200:
        	alert=""" alert ....! are you sure with short codes of station you entered ???
        	if you have doubt please use /code """
        	update.message.reply_text(alert)
        else:
        	
        	update.message.reply_text(text)
  #      logging.info(len(data['trains']))
        	for i in range(0,len(data['trains'])):
        		update.message.reply_text("""train named  """+data['trains'][i]['name']+" with train number: #"+data['trains'][i]['number']+"""
          from  """+data['trains'][i]['from_station']['name']+
          """ to """+ data['trains'][i]['to_station']['name']+ """ 
          starting at """+data['trains'][i]['src_departure_time']+" and arriving at  "+data['trains'][i]['dest_arrival_time']+"""
         total travel time is:"""+data['trains'][i]['travel_time'])
        		
#            logging.info(data['trains'][i]['to_station'])
 #           logging.info(data['trains'][i]['from_station'])
            	
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
def date(bot, update, args):
    if len(args)==5:
        textdate="trains between  " +args[0]+ " and  " +args[1]+"  on date "+args[2]+"-"+args[3]+"-"+args[4]+"  are............."
        #logging.info(text)
        http = urllib3.PoolManager()
        apidate="https://api.railwayapi.com/v2/between/source/"+args[0]+"/dest/"+args[1]+"/date/"+args[2]+"-"+args[3]+"-"+args[4]+"/apikey/"+key+"/"
        logging.info(apidate)
        r = http.request('GET', apidate)
        data = json.loads(r.data.decode('utf-8'))
        if data['response_code'] != 200:
        	alert=""" alert ....! are you sure with short codes of station you entered and the date format ???
        	if you have doubt please use /code 
        	and date format is dd mm yyyy like 08 09 2018 """
        	update.message.reply_text(alert)
        else:
        	
        	update.message.reply_text(textdate)
  #      logging.info(len(data['trains']))
        	for i in range(0,len(data['trains'])):
        		update.message.reply_text("""train named  """+data['trains'][i]['name']+" with train number: #"+data['trains'][i]['number']+"""
          from  """+data['trains'][i]['from_station']['name']+
          """ to """+ data['trains'][i]['to_station']['name']+ """ 
          starting at """+data['trains'][i]['src_departure_time']+" and arriving at  "+data['trains'][i]['dest_arrival_time']+"""
         total travel time is:"""+data['trains'][i]['travel_time'])
        
  #      logging.info(len(data['trains']))
        
    elif len(args) < 5:
        less="""need start and destination and date in dd-mm-yyyy
          eg: /date awy sbc 15 08 2018 """
        update.message.reply_text(less)
        update.message.reply_text(help)
    else:
        great=""""only need start, destination and date
        eg: /date awy sbc 15 08 2018"""
        update.message.reply_text(great)
        update.message.reply_text(help)
def code(bot, update):
    update.message.reply_text(stationcode)
def help(bot, update):
    help="""for listings trains between stations use 
    /trains <start> <destination>
    eg: for travelling from aluva to banglore enter  
    /trains awy sbc 
    for listing short code for stations use
    /code
    for getting trains on particular date use
    /date <start> <dest> <dd> <mm> <yyyy>
    eg: /date awy sbc 08 09 2018
    """
    update.message.reply_text(help)
def main():
    updater = Updater(token)
    j = updater.job_queue
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trains", trains, pass_args=True))
    dp.add_handler(CommandHandler("date",date, pass_args=True))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("code",code))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
