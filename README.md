# LINEBOT 圖書館狀態回報機器人

by 108207442


---

## 專案流程

### 主題介紹與概觀

<aside>
💡 以使用者的角度，黑箱測試

</aside>

1. 發想 ：
    
    由於在遠距的時候很多同學都會到圖書館上綫上課，身爲時間精算師的我往往在上課時剛好壓綫時才趕到圖書舘開遠距，當發現沒有位子時已經爲時已晚，直接被老師被記上了一筆遲到
    
2. ⇒ 功能條列介紹（如何解決發想的問題）
    - 功能
        
        <aside>
        💡 提醒：
        
        - 善用LINE GUI固定格式，非開放問答
        - 要標記功能的INPUT（包含格式（文字？按鈕？））與 OUTPUT（文字？圖表？）至於PROCESS在程式詳解的時候會解析
        </aside>
        
        - 初始設定：
            
            Q：日常前往圖書館時間
            
        - ONCE：
            - 學校系統 - 座位數回報
                - 中正悅讀區及時座位數
                    
                    **INPUT：**（TEXT）中正悅讀區目前座位數
                    
                    <aside>
                    💡 目前僅僅支援中正閲讀區
                    
                    </aside>
                    
                    **OUTPUT：（**IMG）座位數的視覺化圖片
                    
                - 各分館今日入館人數
                    
                    **INPUT：（**TEXT）各分館今日入館人數
                    
                    <aside>
                    💡 目前僅僅支援中正和達賢
                    
                    </aside>
                    
                    **OUTPUT：（**IMG）特定分管人流視覺化圖片
                    
                
                <aside>
                💡 目前只有中正分管有詳細資料，因此本系統導入使用者人流回報的功能
                
                </aside>
                
            - 使用者 - 人流狀況回報
                
                <aside>
                💡 state：擁擠 or 空閑
                
                </aside>
                
                - 特定分管人流回報
                    
                    **INPUT：（**TEXT）{分館} 人流狀況回報
                    
                    <aside>
                    💡 超過多少回報數後改變狀態：
                    
                    如：if 回報數 > 5歸零計數器後改變狀態 
                    
                    </aside>
                    
                    OUPUT：（Confirm template）“擁擠”/“空閑”
                    
                    點選
                    
                    - 擁擠：RETURN
                - 特定分館人流狀況查詢
                    
                    <aside>
                    💡 可以用圖表產製
                    
                    </aside>
                    
                    **INPUT：（**TEXT）{分館} 人流狀況
                    
                    OUPUT：（TEXT）特定分館的人流狀況
                    
                - 所有分管人流回報與建議（去人少的地方）
                    
                    TEXT：所有 目前人流狀況比較
                    
                    OUTPUT：（TEXT）所有分館的人流狀況與建議
                    
            - 開閉舘資訊：
                
                INPUT：（TEXT）所有 今日開閉館資訊
                
                OUTPUT：（TEXT）{分舘} 今日開閉館資訊
                
            - 相關公車動態：
                
                。。。。。
                

### 程式DEMO

<aside>
💡 以使用者的角度，黑箱測試

</aside>

<aside>
💡 這邊可以帶入一些互動（讓同學加line）

</aside>

1. 程式伺服器部署
2. 實作 功能條列介紹之功能

### 程式架構詳解

<aside>
💡 以程式設計師的角度

</aside>

1. 使用工具介紹
    
    函式庫：
    
    - DJANGO：網頁
    - LINEBOT API SDK4 Python：linebot api
    - NOGROK：伺服器
    - BF4：爬蟲
    - 繪圖函式庫（待尋找）
2. 專案架構概述（這些工具如何組合在一起？？運作流程）
    
    ![Untitled](LINEBOT%20%E5%9C%96%E6%9B%B8%E9%A4%A8%E7%8B%80%E6%85%8B%E5%9B%9E%E5%A0%B1%E6%A9%9F%E5%99%A8%E4%BA%BA%208e0c39f3e0504a2dada5e4a7b9bc9b44/Untitled.png)
    
    1. （INPUT）使用者傳入訊息到 LINE官方賬號
    2. （PEOCESS）透過WEBHOOK將訊息傳送至我們建立的server，來進行相關邏輯的處理
    3. （OUTPUT）最終將結果回傳至使用者line賬號
        
        <aside>
        💡 這裏的結果是來自：
        
        - WEBSITE（政大圖書館入館人數）
        - db（資料庫中相關回報成果的資料）
        </aside>
        

1. 資料庫結構解析
    
    Class：Library
    
    - libName：圖書館的名稱
    - libState：圖書館目前人流狀態
    - libRes_**crowded**：回復人數_擁擠
    - libRes_free：回復人數_空閑
    - libInfo：其他事項記錄（如：開閉舘時間）
        
        資料來源：
        
        [開放時間](https://www.lib.nccu.edu.tw/p/404-1000-532.php)
        
    
    models.py
    
    ```python
    from django.db import models
    
    # Create your models here.
    class Library(models.Model):
        def __str__(self):
            return 'MyModel: {}'.format(self.libName)
        # (實際值， 頁面顯示出來的值)
        STATE_TYPE_CHOICE = (
             ('crowded', '擁擠')
            ,('free', '空閒') 
        )
    
        LIBNAME_CHOICE = (
             ('main', '中正')
            ,('dh', '達賢')
            ,('zhongtu', '綜圖')
            ,('shangtu', '商圖') 
        )
    
        # 圖書館名稱
        libName = models.TextField(default="", choices=LIBNAME_CHOICE)
        # 圖書館狀態
        libState = models.TextField(default="free", choices=STATE_TYPE_CHOICE)
        # 圖書館擁擠回報數
        libRes_crowded = models.DecimalField(default=0, max_digits=2, decimal_places=0)
        # 圖書館空閑回報數
        libRes_free = models.DecimalField(default=0, max_digits=2, decimal_places=0)
        # 圖書館資訊
        libInfo = models.TextField(default="")
        created = models.DateTimeField(auto_now_add=True)
        class Meta:
            db_table = "library"
    ```
    
2. 個別模組解析
    1. 模組概覽
    2. 個模組解析
        
        <aside>
        💡 模組的一開始要寫清楚這個模組在幹嘛
        
        </aside>
        
        1. 主程式（view.py）
            
            ```python
            
            ```
            
        2. replyData.py
            
            目的：集中管理所有的回傳訊息
            
            ```python
            
            ```
            
        3. getlib.py
            
            目的：用來爬取學校提供的圖書館動態
            
            <aside>
            💡 包含：
            
            - 達賢/中正 今日入館人數
            - 中正悅讀區 即時座位資訊
            </aside>
            
            ```python
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
            ```
            
3. 程式潛在問題與待改進部分
    1. 提倡公開資料的提供：
        
        目前只有中正圖書舘悅讀區有即使的座位數，因此希望其他分管也能公開相關資料，讓學生前往選擇圖書館時更加的便利
        
    2. 使用者客制化：可以結合資料庫讓不同使用者體驗到客制化的體驗
        
        <aside>
        💡 例如：
        
        - 依位置：不同的策略，最近的圖書館 or 人最少的圖書館？？權重
        - 依習慣：例如在常常去圖書館的日子，自動排程推送訊息
        </aside>
        
    3. 排程：加入排程自動通知
