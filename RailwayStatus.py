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

HELP_TEXT = """
    what this bot can do ..?
    this bot helps to get services offered by  NTES
    maintained by @prinzpiuz 
    for more news subscribe to my channel @princepiuz   
    for help please enter /help 
    source code is available @
    https://github.com/prinzpiuz/RailwayStatusBot
    suggetions and contributions are always welcome
    #FreeAsInFreedom
    NB:as part of privacy this bot never collects or store any kind data of users

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
        		update.message.reply_text("""train named  """+data['trains'][i]['name']+" with train number: <b>"+data['trains'][i]['number']+"""
         </b> from  """+data['trains'][i]['from_station']['name']+
          """ to """+ data['trains'][i]['to_station']['name']+ """ 
          starting at """+data['trains'][i]['src_departure_time']+" and arriving at  "+data['trains'][i]['dest_arrival_time']+"""
         total travel time is:"""+data['trains'][i]['travel_time'],parse_mode=ParseMode.HTML)
        
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
def pnr(bot, update, args):
    http = urllib3.PoolManager()
   # print(args[0])
    PNR="https://api.railwayapi.com/v2/pnr-status/pnr/"+args[0]+"/apikey/"+key+"/"
    logging.debug(PNR)
    r = http.request('GET', PNR)
    data = json.loads(r.data.decode('utf-8'))
    if data['response_code'] != 200:
        alertp="are you sure with your PNR no "+args[0]+" ?"
        update.message.reply_text(alertp)
    else:
        update.message.reply_text("processing .........")
        msg="""your status for PNR no """+args[0]+"""  for journey starting from
        """+ data['boarding_point']['name']+ """ to """+data['reservation_upto']['name']+"""
        in train """+data['train']['name']+""" with no """+data['train']['number']+"""
        in """+ data['journey_class']['name']+"""with following people bellow."""
        update.message.reply_text(msg)
        for i in range(0,len(data['passengers'])):
                print(len(data['passengers']))
                update.message.reply_text("""
           person """ +data['passenger'][i]['no']+""". current status: """+data['passenger'][i]['current_status']+""" 
           and booking status: """+data['passenger'][i]['booking_status'])


def live(bot, update, args):
    """Gives the live position of a train.
    Required args are the train number and the date
    """
    http = urllib3.PoolManager()
    try:
        train_number, date = args
    except ValueError as exc:
        update.message.reply_text(
            'only need train number and date '
            'eg: /live 12046 01-12-2018'
            )
    else:
        # for now we won't implement a date validator
        LIVE = (
            'https://api.railwayapi.com/v2/live'
            '/train/{train_number}'
            '/date/{date}'
            '/apikey/{key}'
            ).format(
                train_number=train_number,
                date=date,
                key=key
                )
        r = http.request('GET', LIVE)
        data = json.loads(r.data.decode('utf-8'))
        if data['response_code'] != 200:
            alert = "something went wrong"
            update.message.reply_text(alert)
        else:
            train_name = data['train']['name']
            position = data['position']
            msg = (
                'Train: {name}\n'
                'Status: {position}'
                ).format(
                    name=train_name,
                    position=position
                    )
            update.message.reply_text(msg)

def arrivals(bot, update, args):
    """Gives list of trains arriving at a station within a window period,
        along with their live status.
    Required args are the train number and the date
    """
    http = urllib3.PoolManager()
    try:
        station_code, hrs = args
    except ValueError as exc:
        update.message.reply_text(
            'only need station code and hours window'
            'eg: /arrivals sbc 2'
            'eg: /arrivals awy 4'
            )
    else:
        # for now we won't implement a date validator
        LIVE = (
            'https://api.railwayapi.com/v2/arrivals'
            '/station/{station}'
            '/hours/{hours}'
            '/apikey/{key}'
            ).format(
                station=station_code,
                hours=hrs,
                key=key
                )
        r = http.request('GET', LIVE)
        data = json.loads(r.data.decode('utf-8'))
        if data['response_code'] != 200:
            alert = "something went wrong"
            update.message.reply_text(alert)
        else:
            arriving_trains = data['trains']
            total_trains = data['total']
            if arriving_trains:
                msg = "Total {} trains arriving during {}".format(total_trains,hrs)
                update.message.reply_text(msg)
                for arr_train in arriving_trains:
                    train_name = arr_train["name"]
                    train_number = arr_train["number"]
                    
                    sch_arr = arr_train["scharr"]
                    act_arr = arr_train["actarr"]
                    delay_arr = arr_train["delayarr"]
                     
                    sched_dep = arr_train["schdep"]
                    act_dep = arr_train["actdep"]
                    delay_dep = arr_train["delaydep"]
                    
                    msg = (
                        'Train: {name}\n'
                        'Train Number: {number}\n'
                        'Scheduled Arrival: {scharr}\n'
                        'Actual Arrival: {actarr}\n'
                        'Delay in Arrival: {delayarr}\n'
                        'Scheduled Departure: {schdep}\n'
                        'Actual Departure: {actdep}\n'
                        'Delay in Departure: {delaydep}'
                        ).format(
                            name = train_name,
                            number = train_number,
                            scharr = sch_arr,
                            actarr = act_arr,
                            delayarr = delay_arr,
                            schdep = sched_dep,
                            actdep = act_dep,
                            delaydep = delay_dep
                            )
                    update.message.reply_text(msg)
            else:
                alert = "No arriving trains during {} hours".format(hrs)
                update.message.reply_text(alert)


def help(bot, update):


    help = """
      available commands and their usage 
      for listings trains between stations use 
      /trains <start> <destination>
      eg: for travelling from aluva to banglore enter 
      /trains awy sbc
      for listing short station codes 
      /code
      for listing trains on particular date
      /date <start> <dest> <dd> <mm> <yyyy>
      eg: /date awy sbc 15 08 2018
      for getting the status of your PNR
      /pnr <pnr no>
      for getting live train status
      /live train# 15-08-2018
      for list trains arriving in a station in comming hrs
      /arrivals sbc 4
      /arrivals awy 2
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
    dp.add_handler(CommandHandler("pnr",pnr,pass_args=True))
    dp.add_handler(CommandHandler("live", live, pass_args=True))
    dp.add_handler(CommandHandler("arrivals", arrivals, pass_args=True))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
