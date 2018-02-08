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
        
        
