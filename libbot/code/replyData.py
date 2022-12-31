from django.conf import settings
from libbot.code.getlib import getLibInfo
from libbot.models import Library
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

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

main_realtime = '''中正悅讀區及時座位數：
A區座位：{}
B區座位：{}
C區座位：{}'''.format(
    getLibInfo()['ava_seats_a']
    ,getLibInfo()['ava_seats_b']
    ,getLibInfo()['ava_seats_c']
)

# numer of people realtime
nops_realtime = '''各分館及時今日入館人數:
中正:{}
達賢:{}
'''.format(
    getLibInfo()['nops_zz']
    ,getLibInfo()['nops_dh']
)
error_text = "現在還不支援這個功能歐~~"

# 設定分館的中英文對照（key : value）
libNameC2E = {
    '中正': 'main',
    '達賢': 'dh',
    '商圖': 'shangtu',
    '綜圖': 'zhongtu'
} 

libNameE2C = {
    'main': '中正',
    'dh': '達賢',
    'shangtu': '商圖',
    'zhongtu': '綜圖'
} 

stateE2C = {
    'free': '空閒',
    'crowded': '擁擠'
}


# 簡化回傳内容的流程
def replyText(event, txt):
    line_bot_api.reply_message(  
         event.reply_token
        ,TextSendMessage(text=txt)
    ) 

def replyConfirm(event, libName):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    line_bot_api.reply_message(  
        event.reply_token
        ,TemplateSendMessage(
            alt_text='人流回報',
            template=ConfirmTemplate(
                text='哈嘍，{}！現在{}分館的人流狀況如何呀？！'.format(profile.display_name, libName),
                actions=[
                    PostbackAction(
                        label='擁擠',
                        display_text='館長{}分館現在人好多QAQ'.format(libName),
                        data='{}&crowded'.format(libName)
                    ),
                    PostbackAction(
                        label='空閒',
                        display_text='館長{}分館現在四下無人嘿嘿嘿'.format(libName),
                        data='{}&free'.format(libName)
                    )
                ]
            )
        )
    ) 