from linebot import (LineBotApi, WebhookHandler)
from linebot import exceptions
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *



def main_template():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            #thumbnail_image_url="https://i.imgur.com/GsVmocY.jpg",
            title="主選單",
            text="請選擇服務",
            actions=[
                
                PostbackTemplateAction(
                    label="找點樂子",
                    data="boaring",
                ),
                
                PostbackTemplateAction(
                    label="肚子餓了",
                    data="hungry",
                ),
                PostbackTemplateAction(
                    label="股票查詢",
                    data="stock",
                )
            ]
        )
    )
    return message
    
def boaring_template():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            #thumbnail_image_url="https://i.imgur.com/GsVmocY.jpg",
            title="娛樂",
            text="請選擇服務",
            actions=[
                PostbackTemplateAction(
                    label="抽圖片",
                    data="getimg",
                ),
                
                PostbackTemplateAction(
                    label="猜拳",
                    data="play",
                ),
                PostbackTemplateAction(
                    label="返回主選單",
                    data="back",
                )
            ]
        )
    )
    return message

def getimg_template():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            #thumbnail_image_url="https://i.imgur.com/GsVmocY.jpg",
            title="抽圖類型",
            text="請選擇類型",
            actions=[
                
                PostbackTemplateAction(
                    label="ACGN",
                    data="acgimg",
                ),
                
                PostbackTemplateAction(
                    label="迷因",
                    data="memeimg",
                ),
                PostbackTemplateAction(
                    label="返回找樂子",
                    data="back",
                )
            ]
        )
    )
    return message

def acgimg_template():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            #thumbnail_image_url="https://i.imgur.com/GsVmocY.jpg",
            title="抽圖",
            text="請選擇類型",
            actions=[
                
                PostbackTemplateAction(
                    label="抽",
                    data="get",
                ),
                
                PostbackTemplateAction(
                    label="返回圖片類型",
                    data="back",
                )
            ]
        )
    )
    return message

def memeimg_template():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            #thumbnail_image_url="https://i.imgur.com/GsVmocY.jpg",
            title="抽圖",
            text="請選擇類型",
            actions=[
                
                PostbackTemplateAction(
                    label="抽",
                    data="get",
                ),
                
                PostbackTemplateAction(
                    label="返回圖片類型",
                    data="back",
                )
            ]
        )
    )
    return message

def play_template():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            #thumbnail_image_url="https://i.imgur.com/GsVmocY.jpg",
            title="猜拳",
            text="猜拳",
            actions=[
                
                PostbackTemplateAction(
                    label="剪刀",
                    data="scissor",
                ),
                
                PostbackTemplateAction(
                    label="石頭",
                    data="stone",
                ),
                
                PostbackTemplateAction(
                    label="布",
                    data="paper",
                ),
                
                PostbackTemplateAction(
                    label="返回找樂子",
                    data="back",
                )
            ]
        )
    )
    return message

def stock_template():
    message = TemplateSendMessage(
        alt_text='好消息來囉～',
        template=ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/GsVmocY.jpg",
            title="股票資訊查詢",
            text="選擇欲查日期及股票名稱",
            actions=[
                DatetimePickerTemplateAction(
                    label="請選擇欲查詢日期",
                    data="stock_date",
                    mode='date',
                    initial='2012-01-01',
                    min = '2012-01-01'
                ),

                PostbackTemplateAction(
                    label="由證券代號(EX:0050)查詢",
                    data="0",
                ),
                
                PostbackTemplateAction(
                    label="由證券名稱(EX:元大台灣50)",
                    data="1",
                ),
                PostbackTemplateAction(
                    label="返回主選單",
                    data="back",
                )
            ]
        )
    )
    return message
