import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests
import urllib.request

import json
    

import pandas as pd
import datetime
from datetime import datetime, timedelta
import math
import time


main_coins = ['bitcoin', 'ethereum']
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjEsInJvbGUiOiJhZG1pbjQiLCJsb2dpbiI6Ik9GRklDRSIsImlhdCI6MTYyNjIwNDU1OSwiZXhwIjoyNjI2MjkwOTU5fQ.5UAdsqGdyZwdJG7hyFoGyD2UM3tT0xQi5n1iCrAImkc'
tele_TOKEN = '1880188697:AAHzKOFN3HqgU5b4672z2RORjT8br9gU0js'
chat_id = '-1001506681242'
# если делаем отчет в день х, то есть баланс на 00:00 дня х. Тогда отчет для дня с 29 на 30, нужны такие даты

    
headers = {'Cookie':'token='+TOKEN}
exchanges = [
    'xt',
    'probit',
    'hitbtc',
    'bitforex',
    'bitmart',
    'hotbit',
    'bibox',
    'ibank',
    'gate',
    'coinsuper',
    'exmarkets',
    'stex',
    'kucoin',
    'crex24',
    'stocks_exchange',
    'p2pb2b',
    'timex',
    'coinsbit',
    'c3'
]


def get_price(coin):
    url = 'https://api.coingecko.com/api/v3/coins/'+ coin
    
        

    while True:
        try:
            s = get_soup(url)
            break
        except(urllib.error.HTTPError):
            return '0','0'
    
    price = s['market_data']['price_change_24h'], s['market_data']['current_price']['usd']
    return price

def get_volume(coin):
    # volumes
    
    #time = datetime.datetime.today().strftime("%Y_%m_%d_%H:%M:%S")
    
   
    url = 'https://api.coingecko.com/api/v3/coins/'+ coin

    while True:
        try:
            s = get_soup(url)
            break
        except(urllib.error.HTTPError):
            text = 'Нет на Геко \n'
            return text
    

       
    text = str(s['market_data']['total_volume']['usd']) + ', '
    
    tickers = s['tickers']
    for ticker in tickers:
        if ticker['market']['identifier'] in exchanges:
            text += ticker['market']['name'] + ': ' + ticker['base'] + ' - ' + ticker['target'] + ': ' + str(ticker['converted_volume']['usd']) + ', ' 

    return text


# def telegram_bot_sendtext(bot_message):
    
#     bot_token = '1880188697:AAHzKOFN3HqgU5b4672z2RORjT8br9gU0js'
#     bot_chatID = '-564875501'
#     send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    
    
#     response = requests.get(send_text)

#     return response.json()




def balance(pairs, time_start, time_close):
    
    text = ''
    ts1 = time_start
    ts2 = time_close
    asset_start = 0
    asset_close = 0
    token_start = 0
    token_close = 0
    
    for pair in pairs:
        data = {'path':pair}
        headers = {'Cookie':'token='+TOKEN}

        response = requests.post("https://app.gotbit.io/api/GetGrafs", data, headers=headers)
        
        
        while True:
            try:
                s = response.json()['left']
                for elem in response.json()['left']:
                    if elem['time'] >= (int(time.mktime(time.strptime(ts1, '%Y-%m-%d %H:%M:%S'))) + 10920):
                        asset_start = elem['value']
                        break
                        
                for elem in response.json()['left']:
                    if elem['time'] >= (int(time.mktime(time.strptime(ts2, '%Y-%m-%d %H:%M:%S'))) + 10920):
                        asset_close = elem['value']
                        break
                        
                        
                text += pair + ' разница балансов: ассеты = ' + str(asset_close - asset_start) +', токены = '
                
                for elem in response.json()['right']:
                    if elem['time'] >= (int(time.mktime(time.strptime(ts1, '%Y-%m-%d %H:%M:%S'))) + 10920):
                        token_start = elem['value']
                        break       
                
                for elem in response.json()['right']:
                    if elem['time'] >= (int(time.mktime(time.strptime(ts2, '%Y-%m-%d %H:%M:%S'))) + 10920):
                        token_close = elem['value']
                        break
                        
                text += str(token_close - token_start) + ', '
                print('1')       
                
                        
                        
                break
            except (KeyError):
                print('KeyError')
                text += pair +': удали это и заполни сам'
                break
    
    return text

def get_bot_info(pairs):
    text =  ''
    for pair in pairs:
        text += '\t' + pair + ': '
        data1 = {'path':pair}
        

        response = requests.post("https://app.gotbit.io/api/GetSettings", data1, headers=headers)
        while True:
            try:
                resp = response.json()
                break
            except:
                print('Decoding problem')
                break
        
        
        
        
        while True:
            try:
                if resp['uniEnable'] == True:
                    text += ' uniDiff = ' + str(resp['uniDiff']) + ', '
                elif resp['virtualWall'] == True:
                    text += ' virtDiff = ' + str(resp['virtDiff']) + ', '
                else:
                    text += ' Стенки не включены '
                text += 'MODE: ' + requests.post("https://app.gotbit.io/api/GetBot", data1, headers=headers).json()['bot']['side'] + '\n'
                break
            except(KeyError):
                text += ' Руками заполни\n'
                break
        
    return text


with open('cs.txt') as f:
    cs = f.read().splitlines()

with open('ts.txt') as f:
    ts = f.read().splitlines()

with open('ps.txt', 'r') as fobj:
    ps = [[str(num) for num in line.split()] for line in fobj]

with open('d_cs.txt') as f:
    d_cs = f.read().splitlines()

with open('ts.txt') as f:
    d_ts = f.read().splitlines()

with open('ps.txt', 'r') as fobj:
    d_ps = [[str(num) for num in line.split()] for line in fobj] 



    
print(d_cs)
print(d_ts)
print(d_ps)









# report()

def report(clients, pairs_for_client, token_names, time_open, time_close, update):
    i = 0
    
    text = ''
    for client in clients:
        
        text = 'Клиент: ' + client + '\n'
        text += '\t 1) график: \n'
        text += '\t цена: изменение цены за 24 часа = ' + str(get_price(token_names[i])[0]) + ', текущая цена = '+ str(get_price(token_names[i])[1]) +'\n'
        text += '\t объем: Общий($) = ' + str(get_volume(token_names[i])) + '\n'
        
        text += '\t балансы: ' + balance(pairs_for_client[i], time_open, time_close) + '\n'
        text += '\t 2) настройки бота\n' + get_bot_info(pairs_for_client[i])
        print(text)
        i += 1
        text += '\t 3) ремонт + стратегия: '
        update.message.reply_text(text)
        
    



def get_soup(url):

    f = urllib.request.urlopen(url)
    
    nyb = f.read()
    mystr = nyb.decode("utf8")
    f.close()
    soup = json.loads(mystr)

    return soup

coins = [
    'pawtocol',
    
    'g999',
    'bitswift',
    'intexcoin',
    'horizondollar',
    'skillchain',
    'exchangecoin',
    'buzzshow',
    'ime-lab',
    'didcoin',
    'phoenix-defi-finance',
    'merchdao',
    'dehive',
    'xsigma',
    'decimal'
        ]



def send_stats():
    # volumes
    vols =[]
    #time = datetime.datetime.today().strftime("%Y_%m_%d_%H:%M:%S")
    text =  '\nVolumes for the last 24h, :\n\n'
    for coin in coins:
        url = 'https://api.coingecko.com/api/v3/coins/'+ coin
        s = get_soup(url)

        client_vols = {'name':'',
                      'volume':''}

        client_vols['name'] = coin
        client_vols['volume'] = s['market_data']['total_volume']['usd']
        vols.append(client_vols)

        text += coin + ' :\n'

        tickers = s['tickers']
        for ticker in tickers:
            if ticker['market']['identifier'] in exchanges:
                text += '\t' + ticker['market']['name'] + ': ' + ticker['base'] + ' - ' + ticker['target'] + ': ' + str(ticker['converted_volume']['usd']) + '\n' 

        text += '\n'
       # print(coin, ' price in usd = ', s['market_data']['current_price']['usd'])

        #print(coin, s['market_data']['total_volume']['usd'])

    text += '\n Current prices in USD :\n\n'
    for coin in coins:
        url = 'https://api.coingecko.com/api/v3/coins/'+ coin
        s = get_soup(url)

        client_prices = {'name':'',
                      'price':''}

        client_prices['name'] = coin
        client_prices['volume'] = s['market_data']['current_price']['usd']
        vols.append(client_vols)
       # print(coin, ' price in usd = ', s['market_data']['current_price']['usd'])
        text += coin + ' - '+str(s['market_data']['current_price']['usd']) + '\n'
        print(coin, s['market_data']['total_volume']['usd'])    

    text += '\n'
    main_coins = ['bitcoin', 'ethereum']
    for coin in main_coins:
        url = 'https://api.coingecko.com/api/v3/coins/'+ coin
        s = get_soup(url)

        client_prices = {'name':'',
                      'price':''}

        client_prices['name'] = coin
        client_prices['volume'] = s['market_data']['current_price']['usd']
        vols.append(client_vols)
       # print(coin, ' price in usd = ', s['market_data']['current_price']['usd'])
        text += coin + ' - '+str(s['market_data']['current_price']['usd']) + '\n'


    return text
    







#PORT = int(os.environ.get('PORT', 8443))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    
    print(update.message.date)
    print(len(context.args))
    update.message.reply_text(str(update.message.date))


def help(update, context):
    """Send a message when the command /help is issued."""
    tt = send_stats()
    update.message.reply_text(tt)


def morn(update, context):
    
    t1 = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d") + ' 15:00:00'
    t2 = datetime.today().strftime("%Y-%m-%d") + ' 07:00:00'
    print(t1, t2)
    update.message.reply_text('Выгрузка началась')
    report(cs , ps, ts, t1, t2, update) 
    report (d_cs, d_ps, d_ts, t1, t2, update)
    

def eve(update, context):
    t1 = datetime.today().strftime("%Y-%m-%d") + ' 07:00:00'
    t2 = datetime.today().strftime("%Y-%m-%d") + ' 15:00:00'
    print(t1, t2)
    update.message.reply_text('Выгрузка началась')
    report(cs , ps, ts, t1, t2, update) 
    report (d_cs, d_ps, d_ts, t1, t2, update)

def ourmorn(update, context):
    t1 = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d") + ' 15:00:00'
    t2 = datetime.today().strftime("%Y-%m-%d") + ' 07:00:00'
    print(t1, t2)
    update.message.reply_text('Выгрузка началась')
    report(cs , ps, ts, t1, t2, update) 
    

def oureve(update, context):
    t1 = datetime.today().strftime("%Y-%m-%d") + ' 07:00:00'
    t2 = datetime.today().strftime("%Y-%m-%d") + ' 15:00:00'
    print(t1, t2)
    update.message.reply_text('Выгрузка началась')
    report(cs , ps, ts, t1, t2, update) 
    

def dimamorn(update, context):
    t1 = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d") + ' 15:00:00'
    t2 = datetime.today().strftime("%Y-%m-%d") + ' 07:00:00'
    print(t1, t2)
    update.message.reply_text('Выгрузка началась')
    
    report (d_cs, d_ps, d_ts, t1, t2, update)

def dimaeve(update, context):
    t1 = datetime.today().strftime("%Y-%m-%d") + ' 07:00:00'
    t2 = datetime.today().strftime("%Y-%m-%d") + ' 15:00:00'
    print(t1, t2)
    update.message.reply_text('Выгрузка началась')
    
    report (d_cs, d_ps, d_ts, t1, t2, update)


def mypaireve(update, context):
    client = []
    pairs = []
    token = []
    if len(context.args) >= 3:
        client.append(context.args[0])
        token.append(context.args[1])
        pair = []
        for i in range (2, len(context.args)):
            pair.append(context.args[i])
        pairs.append(pair)

        t1 = datetime.today().strftime("%Y-%m-%d") + ' 07:00:00'
        t2 = datetime.today().strftime("%Y-%m-%d") + ' 15:00:00'
        print(t1, t2)
        update.message.reply_text('Выгрузка началась')
        
        report (client, pairs, token, t1, t2, update)
    else:
        update.message.reply_text('Плохой запрос, бро. Нужно: TICKER token_name_from_coingecko LEFT1_RIGHT1_exchange1 ... LEFTn_RIGHTn_exchangen')
        return

def mypairmorn(update, context):
    client = []
    pairs = []
    token = []
    if len(context.args) >= 3:
        client.append(context.args[0])
        token.append(context.args[1])
        pair = []
        for i in range (2, len(context.args)):
            pair.append(context.args[i])
        pairs.append(pair)

        t1 = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d") + ' 15:00:00'
        t2 = datetime.today().strftime("%Y-%m-%d") + ' 07:00:00'
        print(t1, t2)
        update.message.reply_text('Выгрузка началась')
        
        report (client, pairs, token, t1, t2, update)
    else:
        update.message.reply_text('Плохой запрос, бро. Нужно: TICKER token_name_from_coingecko LEFT1_RIGHT1_exchange1 ... LEFTn_RIGHTn_exchangen')
        return

def addpairgrant(update, context):
    if len(context.args) >= 3:
        cs.append(context.args[0])
        ts.append(context.args[1])
        pair = []
        text = ''
        for i in range (2, len(context.args)):
            pair.append(context.args[i])
            if i != (len(context.args) - 1):
                text += context.args[i] + ' '
            else:
                text += context.args[i]
        ps.append(pair)

        with open("cs.txt", "a") as myfile:
            myfile.write('\n' + context.args[0])
        with open("ts.txt", "a") as myfile:
            myfile.write('\n' + context.args[1])
        with open("ps.txt", "a") as myfile:
            myfile.write('\n' + text)

        update.message.reply_text('Удачно записана новая пара')

    else:
        update.message.reply_text('Плохой запрос, бро. Нужно: TICKER token_name_from_coingecko LEFT1_RIGHT1_exchange1 ... LEFTn_RIGHTn_exchangen')
        return

def addpairdima(update, context):
    if len(context.args) >= 3:
        d_cs.append(context.args[0])
        d_ts.append(context.args[1])
        pair = []
        text = ''
        for i in range (2, len(context.args)):
            pair.append(context.args[i])
            if i != (len(context.args) - 1):
                text += context.args[i] + ' '
            else:
                text += context.args[i]
        d_ps.append(pair)

        with open("d_cs.txt", "a") as myfile:
            myfile.write('\n' + context.args[0])
        with open("d_ts.txt", "a") as myfile:
            myfile.write('\n' + context.args[1])
        with open("d_ps.txt", "a") as myfile:
            myfile.write('\n' + text)

        update.message.reply_text('Удачно записана новая пара')

    else:
        update.message.reply_text('Плохой запрос, бро. Нужно: TICKER token_name_from_coingecko LEFT1_RIGHT1_exchange1 ... LEFTn_RIGHTn_exchangen')
        return 

def dimapairs(update, context):
    with open('d_ps.txt', 'r') as fobj:
        pairs = [[str(num) for num in line.split()] for line in fobj] 
    update.message.reply_text(str(pairs))

def grantpairs(update, context):
    with open('ps.txt', 'r') as fobj:
        pairs = [[str(num) for num in line.split()] for line in fobj] 
    update.message.reply_text(str(pairs))


        

def echo(update, context):
    """Echo the user message."""
    if (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI') and (update.message.from_user['id']==666165975):
        update.message.reply_text('Ты себя видел?')
    elif (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI') and (update.message.from_user['id']==553439580):
        update.message.reply_text('Здорово, отец!')
    elif (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI') and (update.message.from_user['id']==1649362951):
        update.message.reply_text('Я, товарищ ефрейтор')
    elif (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI') and (update.message.from_user['id']==858240517):
        update.message.reply_text('Привет, Саша!')
    elif (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI') and (update.message.from_user['id']==1005293020):
        update.message.reply_text('Привет, Димас!')
    elif (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI'):
        textu = str(update.message)
        update.message.reply_text(textu)
    
# av_times = {}
# while True:
#     try:
#         chats_df = pd.read_csv('av_times.csv')
#         chats = chats_df.columns
#         for chat in chats:
#             av_times[chat] = [chats_df[chat][0], chats_df[chat][1]]
#         break
#     except(FileNotFoundError):
#         chats= []
#         break





# def av_time(update , context):
#     # if update.message['chat']['id'] in chats:
#     #     message_time = update.message['date']
#     print(update.message['chat'])
#     if update.message['chat']['title'] not in chats: 
#         t = update.message['date'].timestamp()
#         av_times[update.message['chat']['title']] = [t, 0]
#         chats.append(update.message['chat']['title'])
#         print(av_times)

#     else:
#         t_new = update.message['date'].timestamp()
#         if (t_new - av_times[update.message['chat']['title']][0]) > 600:
#             av_times[update.message['chat']['title']][1] = t_new - av_times[update.message['chat']['title']][0]
#         av_times[update.message['chat']['title']][0] = t_new

    

    # df = pd.DataFrame.from_records(av_times)
    # df.to_csv('av_times.csv')   

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Произошла ошибка, пингуй Валеру')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(tele_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("morn", morn))
    dp.add_handler(CommandHandler("eve", eve))
    dp.add_handler(CommandHandler("dimaeve", dimaeve))
    dp.add_handler(CommandHandler("dimamorn", dimamorn))
    dp.add_handler(CommandHandler("oureve", oureve))
    dp.add_handler(CommandHandler("ourmorn", ourmorn))
    dp.add_handler(CommandHandler("mypaireve", mypaireve))
    dp.add_handler(CommandHandler("mypaireve", mypairmorn))
    dp.add_handler(CommandHandler("addpairgrant", addpairgrant))
    dp.add_handler(CommandHandler("addpairgdima", addpairdima))
    dp.add_handler(CommandHandler("dimapairs", dimapairs))
    dp.add_handler(CommandHandler("grantpairs", grantpairs))
    # dp.add_handler(CommandHandler("ourmorn", ourmorn))
    # dp.add_handler(CommandHandler("oureve", oureve))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, av_time))
    dp.add_handler(MessageHandler(Filters.text, echo))
    
    # log all errors
    dp.add_error_handler(error)

    
    print('shit')  
    

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.

    updater.start_polling()
    updater.idle()
    
    

if __name__ == '__main__':
    main()