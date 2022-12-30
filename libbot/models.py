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