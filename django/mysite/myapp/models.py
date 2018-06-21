from django.db import models

# Create your models here.

class Table1(models.Model):
    序号 = models.AutoField(primary_key=True)
    链接 = models.TextField(blank=True)
    线报 = models.TextField(blank=True)
    权限 = models.TextField(blank=True)
    时间 = models.TextField(blank=True)


    class Meta:
        #定义该 model 在数据中的表名称
        db_table = 'table1'
    def __str__(self):
        return "%s,%s,%s,%s" % (self.链接,self.线报,self.权限,self.时间)
        
class JDcoupon(models.Model):
    序号 = models.AutoField(primary_key=True)
    价值 = models.FloatField(blank=True)
    品类 = models.TextField(blank=True)
    限制 = models.FloatField(blank=True)
    图片链接 = models.TextField(blank=True)
    领取链接 = models.TextField(blank=True)
    页面链接 = models.TextField(blank=True)
    时间 = models.TextField(blank=True)
    折扣率 = models.FloatField(blank=True)

    class Meta:
        #定义该 model 在数据中的表名称
        db_table = 'jdcoupon'
    def __str__(self):
        return "%f,%s,%f,%s,%s,%s,%s,%f" % (self.价值,self.品类,self.限制,self.图片链接,self.领取链接,self.页面链接,self.时间,self.折扣率)
    

