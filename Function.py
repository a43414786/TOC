from linebot import exceptions
from linebot.models import *
from templates import *
from images import acgimgs,memeimgs
import numpy as np
import os
import pickle as pkl
import requests
from bs4 import BeautifulSoup

def stock_data(date,id = '0050',name = '元大台灣50',mode = 0):
    date = date.replace('-','')
    try:
        if(mode):
            labels = ['證券代號','證券名稱','成交股數','成交筆數','成交金額','開盤價','最高價','最低價',
                '收盤價','漲跌(+/-)','漲跌價差','最後揭示買價','最後揭示買量','最後揭示賣價','最後揭示賣量','本益比']
            if(date + '.pkl' in os.listdir('stock_infos')):
                data = pkl.load(open(os.path.join('stock_infos',date + '.pkl'),'rb'))
                if "很抱歉，沒有符合條件的資料!" in data:
                    return "很抱歉，沒有符合條件的資料!"
                result = ''
                for i in data:
                    if name in i[1]:
                        for j in range(len(labels)):
                            result = result + labels[j] + ' : ' + i[j] + '\n'
                if(result == ''):
                    return "很抱歉，沒有符合條件的資料!"
                else:
                    return result


            url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&date=' + str(date) + '&type=ALLBUT0999'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if ('很抱歉，沒有符合條件的資料!' in soup.text):
                pkl.dump("很抱歉，沒有符合條件的資料!",open(os.path.join('stock_infos',date + '.pkl'),'wb'))
                return "很抱歉，沒有符合條件的資料!"
            table = soup.find_all('table')[8]
            columnNames = table.find('thead').find_all('tr')[2].find_all('td')
            columnNames = [elem.getText() for elem in columnNames]
            rowDatas = table.find('tbody').find_all('tr')
            rows = []
            
            for row in rowDatas:
                    rows.append([elem.getText().replace(',', ',') for elem in row.find_all('td')])
            pkl.dump(rows,open(os.path.join('stock_infos',date + '.pkl'),'wb'))
            result = ''
            for i in rows:
                if name in i[1]:
                    for j in range(len(labels)):
                        result = result + labels[j] + ' : ' + i[j] + '\n'
            if(result == ''):
                return "很抱歉，沒有符合條件的資料!"
            else:
                return result
        else:
            labels = ['證券代號','證券名稱','成交股數','成交筆數','成交金額','開盤價','最高價','最低價',
                '收盤價','漲跌(+/-)','漲跌價差','最後揭示買價','最後揭示買量','最後揭示賣價','最後揭示賣量','本益比']
            if(date + '.pkl' in os.listdir('stock_infos')):
                data = pkl.load(open(os.path.join('stock_infos',date + '.pkl'),'rb'))
                if "很抱歉，沒有符合條件的資料!" in data:
                    return "很抱歉，沒有符合條件的資料!"
                result = ''
                for i in data:
                    if id in i[0]:
                        for j in range(len(labels)):
                            result = result + labels[j] + ' : ' + i[j] + '\n'
                if(result == ''):
                    return "很抱歉，沒有符合條件的資料!"
                else:
                    return result


            url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&date=' + str(date) + '&type=ALLBUT0999'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup.text)
            if ('很抱歉，沒有符合條件的資料!' in soup.text):
                pkl.dump("很抱歉，沒有符合條件的資料!",open(os.path.join('stock_infos',date + '.pkl'),'wb'))
                return "很抱歉，沒有符合條件的資料!"
            table = soup.find_all('table')[8]
            columnNames = table.find('thead').find_all('tr')[2].find_all('td')
            columnNames = [elem.getText() for elem in columnNames]
            rowDatas = table.find('tbody').find_all('tr')
            rows = []
            
            for row in rowDatas:
                    rows.append([elem.getText().replace(',', ',') for elem in row.find_all('td')])
            pkl.dump(rows,open(os.path.join('stock_infos',date + '.pkl'),'wb'))
            result = ''
            for i in rows:
                if id in i[0]:
                    for j in range(len(labels)):
                        result = result + labels[j] + ' : ' + i[j] + '\n'
            if(result == ''):
                return "很抱歉，沒有符合條件的資料!"
            else:
                return result
    except exceptions as e:
        return "很抱歉，沒有符合條件的資料!"

Stock_date = ""
Stock_mode = 0

def boaring(msg,cur_fsm,line_bot_api,event):
    if "抽圖" in msg:
        cur_fsm.getimg()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("選擇抽圖類型"))
    elif "猜拳" in msg:
        cur_fsm.play()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("來玩猜拳吧！"))
    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    elif "選單" in msg:
        line_bot_api.reply_message(event.reply_token, boaring_template())

def getimg(msg,cur_fsm,line_bot_api,event):
    if "acg" in msg:
        cur_fsm.acg()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("準備抽ACGN"))
    
    elif "meme" in msg:
        cur_fsm.meme()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("準備抽迷因"))

    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    elif "選單" in msg:
        line_bot_api.reply_message(event.reply_token, getimg_template())

def acgimg(msg,cur_fsm,line_bot_api,event):
    if "抽" in msg:
        img_idx = np.random.randint(0,len(acgimgs),10)
        columns = []
        for i in range(10):
            columns.append(
                ImageCarouselColumn(
                    image_url=acgimgs[img_idx[i]],
                    action=URITemplateAction(
                        uri=acgimgs[img_idx[i]]
                    )
                )
            )

        message = TemplateSendMessage(
            alt_text='圖片旋轉木馬',
            template=ImageCarouselTemplate(
                columns=columns
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    elif "選單" in msg:
        line_bot_api.reply_message(event.reply_token, acgimg_template())

def memeimg(msg,cur_fsm,line_bot_api,event):
    if "抽" in msg:
        img_idx = np.random.randint(0,len(memeimgs),10)
        columns = []
        for i in range(10):
            columns.append(
                ImageCarouselColumn(
                    image_url=memeimgs[img_idx[i]],
                    action=URITemplateAction(
                        uri=memeimgs[img_idx[i]]
                    )
                )
            )

        message = TemplateSendMessage(
            alt_text='圖片旋轉木馬',
            template=ImageCarouselTemplate(
                columns=columns
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    elif "選單" in msg:
        line_bot_api.reply_message(event.reply_token, memeimg_template())

def play(msg,cur_fsm,line_bot_api,event):
    if "剪刀" in msg:
        a = np.random.randint(0,3)
        if(a == 0):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出剪刀，平手呢"))
        elif(a == 1):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出石頭，我贏啦"))
        elif(a == 2):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出布，你贏了"))
    elif "石頭" in msg:
        a = np.random.randint(0,3)
        if(a == 0):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出剪刀，你贏了"))
        elif(a == 1):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出石頭，平手呢"))
        elif(a == 2):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出布，我贏啦"))
    elif "布" in msg:
        a = np.random.randint(0,3)
        if(a == 0):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出剪刀，我贏啦"))
        elif(a == 1):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出石頭，你贏了"))
        elif(a == 2):
            line_bot_api.reply_message(event.reply_token, TextSendMessage("我出布，平手呢"))
    elif "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    elif "選單" in msg:
        line_bot_api.reply_message(event.reply_token, play_template())

def signup(msg,cur_fsm,line_bot_api,event):
    if '註冊' in msg:
        cur_fsm.signup()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入姓名"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請註冊後開始使用(輸入\"註冊\"以開始註冊)"))

def name(msg,cur_fsm,line_bot_api,event,register):    
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("返回"))
    else:
        register['name'] = msg
        cur_fsm.name()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入Email"))

def mail(msg,cur_fsm,line_bot_api,event,register):
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入姓名"))
    else:
        register['mail'] = msg
        cur_fsm.check()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("姓名:"+register['name']+"\nEmail:"+register['mail']+"\n請問正確嗎?(yes or no)"))
        
def check(msg,cur_fsm,line_bot_api,event):
    if "yes" in msg:
        cur_fsm.done()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("註冊成功，可以開始使用了!"))
    elif 'no' in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入Email"))
        
def main(msg,cur_fsm,line_bot_api,event):

    if '選單' in msg:
        line_bot_api.reply_message(event.reply_token, main_template())

    elif '無聊' in msg:
        cur_fsm.boaring()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("來點娛樂吧!"))
    elif '餓' in msg:
        cur_fsm.hungry()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("想吃什麼呢?"))
    elif '股票' in msg:
        cur_fsm.stock()
        line_bot_api.reply_message(event.reply_token, stock_template())#TextSendMessage("請輸入欲查詢日期(EX:2022/01/01)"))

def stock(msg,cur_fsm,line_bot_api,event):
    global Stock_date
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入欲查詢日期(EX:2022/01/01)"))
    elif "選單" in msg:
        line_bot_api.reply_message(event.reply_token, stock_template())
    else:
        Stock_date = msg
        cur_fsm.stock_date()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("由證券代號(EX:0050)請輸入0\n由證券名稱(EX:元大台灣50)請輸入1"))
    
def stock_date(msg,cur_fsm,line_bot_api,event):
    global Stock_mode
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("由證券代號(EX:0050)請輸入0\n由證券名稱(EX:元大台灣50)請輸入1"))
    elif "0" in msg:
        Stock_mode = 0
        cur_fsm.stock_id()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入證券代號(EX:0050)"))
    elif "1" in msg:
        Stock_mode = 1
        cur_fsm.stock_name()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入證券名稱(EX:元大台灣50)"))
     
def stock_id(msg,cur_fsm,line_bot_api,event):
    global Stock_date
    global Stock_mode
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入證券代號(EX:0050)"))
    else:
        cur_fsm.info()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(stock_data(Stock_date,msg,msg,Stock_mode) + "\n輸入'結束'返回日期選取\n可繼續輸入證券代號查詢"))

def stock_name(msg,cur_fsm,line_bot_api,event):
    global Stock_date
    global Stock_mode
    if "返回" in msg:
        cur_fsm.back()
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入證券名稱(EX:元大台灣50)"))
    else:
        cur_fsm.info()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(stock_data(Stock_date,msg,msg,Stock_mode) + "\n輸入'結束'返回日期選取\n可繼續輸入證券名稱查詢"))

def stock_end(msg,cur_fsm,line_bot_api,event):
    global Stock_mode
    if '結束' in msg:
        cur_fsm.end()
        line_bot_api.reply_message(event.reply_token, stock_template())
    else:
        cur_fsm.back()
        if(Stock_mode):
            stock_name(msg,cur_fsm,line_bot_api,event)
        else:
            stock_id(msg,cur_fsm,line_bot_api,event)