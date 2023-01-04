from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging
# 啓用正規表示法
import re
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, 
    TextSendMessage, 
    TemplateSendMessage, 
    ConfirmTemplate, 
    PostbackAction, 
    MessageAction,
    PostbackEvent,
    QuickReply,
    QuickReplyButton,
)
from libbot.code.replyData import *
from libbot.models import Library
import requests
from bs4 import BeautifulSoup 
logging.basicConfig(level=logging.INFO)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


 
@csrf_exempt
def callback(request):
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
                if event.message.text == "中正悅讀區即時座位數":
                    replyText(event, main_realtime)
                elif event.message.text == "各分館即時今日入館人數":
                    replyText(event, nops_realtime)
                elif event.message.text == "人流回報":
                    line_bot_api.reply_message(  
                        event.reply_token
                        ,TextSendMessage(text='你要回報的是那個分館呢？？',
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(label="中正分館", text="中正分館人流回報")),
                                QuickReplyButton(action=MessageAction(label="達賢分館", text="達賢分館人流回報")),
                                QuickReplyButton(action=MessageAction(label="商圖分館", text="商圖分館人流回報")),
                                QuickReplyButton(action=MessageAction(label="綜圖分館", text="綜圖分館人流回報")),
                            ]))
                    ) 
                elif event.message.text == "中正分館人流回報":
                    replyConfirm(event, "中正")
                elif event.message.text == "達賢分館人流回報":
                    replyConfirm(event, "達賢")
                elif event.message.text == "商圖分館人流回報":
                    replyConfirm(event, "商圖")
                elif event.message.text == "綜圖分館人流回報":
                    replyConfirm(event, "綜圖")
                elif event.message.text == "各分館人流狀況":
                    libObjs = Library.objects.all()
                    lib_msg = '各分館的狀況如下\n'
                    for libObj in libObjs:
                        lib_name = libNameE2C[libObj.libName]
                        lib_state = stateE2C[libObj.libState]
                        lib_msg += "{}分館：目前為{}\n".format(lib_name, lib_state)
                    replyText(event, lib_msg)
                else:
                    replyText(event, error_text)
            elif isinstance(event, PostbackEvent):
                # 資料格式（分館&狀態）
                data = event.postback.data
                libName = data.split("&")[0]
                state = data.split("&")[1] 
                print(libName, state)
                try:
                    # 到資料庫當中進行搜尋該圖書館的info
                    libObj = Library.objects.get(libName=libNameC2E[libName])
                    crowed_sum = libObj.libRes_crowded
                    free_sum = libObj.libRes_free
                    if state == 'crowded':
                        if crowed_sum <= 4:
                            libObj.libRes_crowded+=1
                            replyText(event, "收到！！！很擁擠")
                        else:
                            libObj.libRes_crowded = 0
                            libObj.libState = "crowded"
                            replyText(event, "收到！！！很擁擠")
    
                        libObj.save()
                    else:
                        if free_sum <= 4:
                            libObj.libRes_free+=1
                            replyText(event, "收到！！！很空閒")
                        else:
                            libObj.libRes_free = 0
                            libObj.libState = "free"
                            replyText(event, "收到！！！很空閒")
                        libObj.libRes_free+=1
                        libObj.save()
                except:
                    print("資料庫操作出現問題")
            else:
                logging.debug("這個event還不行處理哦！！")
                

        return HttpResponse()
    else:
        return HttpResponseBadRequest()