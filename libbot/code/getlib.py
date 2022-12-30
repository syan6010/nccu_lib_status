import requests
from bs4 import BeautifulSoup 

def getLibInfo():
    html = requests.get("https://www.lib.nccu.edu.tw/")
    soup = BeautifulSoup(html.text, "html.parser")
    # number of people（main：hongzheng， dh: daxian）
    nops = soup.select("div.addCounter span.addNum")
    nops_zz, nops_dh = nops[0].text, nops[1].text
    # Available Seats B1 of Main Lib.
    ava_seats = soup.select("div.emptySeats span.addNum")
    ava_seats_a, ava_seats_b, ava_seats_c  = ava_seats[0].text, ava_seats[1].text, ava_seats[2].text
    return {
         'nops_zz': nops_zz
        ,'nops_dh': nops_dh
        ,'ava_seats_a': ava_seats_a
        ,'ava_seats_b': ava_seats_b
        ,'ava_seats_c': ava_seats_c
    }