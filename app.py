from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


from Function import *
import os
import numpy as np

import fsm
import images


acgimgs = images.acgimgs
memeimgs = images.memeimgs

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('q18qYvTXmmAD0Ev66VoXVyvthWfLlCzH8SCvRSGhlnn2J10R5jSSYzltc8+AEGBEUVtl1eyH1z/IpzB+fQfekgVYouVVdXJKax6eKma+BNTCrWpXRreCYBQ/x+zpbbal9bPyeH2dT5Oxw5bOhuAxpwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('94cce48d9ade3892eb402445eb3fa676')


fsms = []

fsm.create_fsm()

def check_regist(uid):
    for i in fsms:
        if(i['uid'] == uid):
            return i
    new_fsm = fsm.create_fsm()
    new = {"uid":uid,"fsm":new_fsm,"name":'',"mail":''}
    fsms.append(new)
    return new

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    uid=event.source.user_id
    register = check_regist(uid)
    cur_fsm = register['fsm']
    
    if(cur_fsm.state == "boaring"):

        boaring(msg,cur_fsm,line_bot_api,event)

    elif(cur_fsm.state == "getimg"):

        getimg(msg,cur_fsm,line_bot_api,event)

    elif(cur_fsm.state == "acgimg"):

        acgimg(msg,cur_fsm,line_bot_api,event)

    elif(cur_fsm.state == "memeimg"):

        memeimg(msg,cur_fsm,line_bot_api,event)

    elif(cur_fsm.state == "play"):
        
        play(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == "signup":
        
        signup(msg,cur_fsm,line_bot_api,event)
        
    elif cur_fsm.state == "name":

        name(msg,cur_fsm,line_bot_api,event,register)
    
    elif cur_fsm.state == "mail":
        
        mail(msg,cur_fsm,line_bot_api,event,register)    
    
    elif cur_fsm.state == "check":

        check(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'main':
        
        main(msg,cur_fsm,line_bot_api,event)

    
    elif cur_fsm.state == 'stock':

        stock(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_date':

        stock_date(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_id':

        stock_id(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_name':

        stock_name(msg,cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_end':

        stock_end(msg,cur_fsm,line_bot_api,event)

    


    

@handler.add(PostbackEvent)
def handle_message(event):
    uid=event.source.user_id
    register = check_regist(uid)
    cur_fsm = register['fsm']
    
    if(cur_fsm.state == "boaring"):

        if(event.postback.data == 'getimg'):
            cur_fsm.getimg()
            line_bot_api.reply_message(event.reply_token,getimg_template())

        elif(event.postback.data == 'play'):
            cur_fsm.play()
            line_bot_api.reply_message(event.reply_token,play_template())
            
        elif(event.postback.data == 'back'):
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token,main_template())
            
        
    
    elif(cur_fsm.state == "getimg"):

        if(event.postback.data == 'acgimg'):
            cur_fsm.acg()
            line_bot_api.reply_message(event.reply_token,acgimg_template())

        elif(event.postback.data == 'memeimg'):
            cur_fsm.meme()
            line_bot_api.reply_message(event.reply_token,memeimg_template())
            
        elif(event.postback.data == 'back'):
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token,boaring_template())

    elif(cur_fsm.state == "acgimg"):

        if(event.postback.data == 'get'):
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

        elif(event.postback.data == 'back'):
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token, getimg_template())
    
    elif(cur_fsm.state == "memeimg"):
        if(event.postback.data == 'get'):
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

        elif(event.postback.data == 'back'):
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token, getimg_template())
    
    elif(cur_fsm.state == "play"):
        
        if(event.postback.data == 'scissor'):
            play('剪刀',cur_fsm,line_bot_api,event)
        elif(event.postback.data == 'stone'):
            play('石頭',cur_fsm,line_bot_api,event)
        elif(event.postback.data == 'paper'):
            play('布',cur_fsm,line_bot_api,event)
        elif(event.postback.data == 'back'):
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token, boaring_template())
    
     
    elif cur_fsm.state == 'main':
    
        if(event.postback.data == 'boaring'):
            cur_fsm.boaring()
            line_bot_api.reply_message(event.reply_token,boaring_template())
        elif(event.postback.data == 'stock'):
            cur_fsm.stock()
            line_bot_api.reply_message(event.reply_token,stock_template())

    elif cur_fsm.state == 'stock':

        if(event.postback.data == 'back'):
            cur_fsm.back()
            line_bot_api.reply_message(event.reply_token,main_template())
        else:
            stock(event.postback.params['date'],cur_fsm,line_bot_api,event)

    elif cur_fsm.state == 'stock_date':

        stock_date(event.postback.data,cur_fsm,line_bot_api,event)
    
    




@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
