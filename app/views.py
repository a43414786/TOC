from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,ImageSendMessage

from TOCProject import settings
import numpy as np

from static import imgs
from app.models import *

import os

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

static_path = settings.HTTP_PATH+"/static"
acgimgs = imgs.get_acgimgs()

richMenuId = "richmenu-356df9a2392ca5ad6453ccfe54a5ed7c"

@csrf_exempt
def callback(request):
    global richMenuId
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                #line_bot_api.link_rich_menu_to_user(1,"richmenu-e7ee652e5a43992faa8a37c48ef95d4c")
                mtext=event.message.text
                uid=event.source.user_id
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=profile.picture_url
                message=[]
                if User_Info.objects.filter(uid=uid).exists()==False:
                    User_Info.objects.create(uid=uid,name=name,pic_url=pic_url,mtext=mtext)
                    message.append(TextSendMessage(text='會員資料新增完畢'))
                '''
                elif User_Info.objects.filter(uid=uid).exists()==True:
                    message.append(TextSendMessage(text='已經有建立會員資料囉'))
                    user_info = User_Info.objects.filter(uid=uid)
                    for user in user_info:
                        info = 'UID=%s\nNAME=%s\n大頭貼=%s'%(user.uid,user.name,user.pic_url)
                        message.append(TextSendMessage(text=info))
                '''
                if(richMenuId == "richmenu-356df9a2392ca5ad6453ccfe54a5ed7c"):
                    richMenuId = "richmenu-e7ee652e5a43992faa8a37c48ef95d4c"
                    line_bot_api.link_rich_menu_to_user(uid,"richmenu-e7ee652e5a43992faa8a37c48ef95d4c")
                else:
                    richMenuId = "richmenu-356df9a2392ca5ad6453ccfe54a5ed7c"
                    line_bot_api.link_rich_menu_to_user(uid,"richmenu-356df9a2392ca5ad6453ccfe54a5ed7c")
                img = acgimgs[np.random.randint(0,len(acgimgs))]
                #message.append(TextSendMessage(text=mtext))
                message.append(ImageSendMessage(original_content_url=static_path+"/acgimg/"+img ,preview_image_url=static_path+"/acgimg/"+img))
                line_bot_api.reply_message(event.reply_token,message)


        return HttpResponse()
    else:
        return HttpResponseBadRequest()