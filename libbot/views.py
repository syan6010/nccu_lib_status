from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from libbot.code.replyData import *
import requests
from bs4 import BeautifulSoup 
 
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
# 簡化回傳文字的流程
def replyText(event, txt):
    line_bot_api.reply_message(  
        event.reply_token,
        TextSendMessage(text=txt)
    ) 

 
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
                if event.message.text == "中正悅讀區目前座位數":
                    replyText(event, main_realtime)
                elif event.message.text == "各分館今日入館人數":
                    replyText(event, nops_realtime)
                else:
                    replyText(event, error_text)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()