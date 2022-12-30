from libbot.code.getlib import getLibInfo

main_realtime = '''中正悅讀區目前座位數：
A區座位：{}
B區座位：{}
C區座位：{}'''.format(
    getLibInfo()['ava_seats_a']
    ,getLibInfo()['ava_seats_b']
    ,getLibInfo()['ava_seats_c']
)

# numer of people realtime
nops_realtime = '''各分館今日入館人數:
中正:{}
達賢:{}
'''.format(
    getLibInfo()['nops_zz']
    ,getLibInfo()['nops_dh']
)
error_text = "現在還不支援這個功能歐~~"