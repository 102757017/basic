from django.db import models

# Create your models here.

class Table1(models.Model):
    链接 = models.TextField(primary_key=True)
    线报 = models.TextField(blank=True, null=True)
    权限 = models.TextField(blank=True, null=True)
    时间 = models.TextField(blank=True, null=True)


    class Meta:      
        db_table = 'table1'
    def __str__(self):
        return "%s,%s,%s,%s" % (self.链接,self.线报,self.权限,self.时间)
        
        