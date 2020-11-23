from django.db import models

# Create your models here.
class books(models.Model):
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=255)
    isbn=models.CharField(max_length=255)
    publisher=models.CharField(max_length=255)
    publication_year=models.DateField('publication year')  #出版日期
    last_modified_date=models.DateField('last modified date')   #修改日期
    created_date=models.DateField(auto_now=True)
    created_at=models.TimeField(auto_now=True)  #發建立時間  (自動獲取目前時間)
    update_at=models.TimeField(auto_now=True)  #發建立時間  (自動獲取目前時間)

    def _str_(self):
        return self.title
