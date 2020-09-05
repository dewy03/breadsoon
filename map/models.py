from django.db import models

# Create your models here.

class Bakery_Info(models.Model):
    Bakery_name = models.CharField(max_length=50)           # 빵집 이름
    Bakery_address = models.CharField(max_length=100)       # 빵집 주소
    Bakery_menu = models.CharField(max_length=50)           # 빵집 메뉴

    def __str__(self):
        return self.Bakery_name

class Bakery_Location(models.Model):
    #Bakery = models.CharField(max_length=50,null=True)
    info = models.OneToOneField(Bakery_Info,on_delete=models.CASCADE,primary_key=True)
    Latitude = models.FloatField()      #위도
    Longitude = models.FloatField()     #경도

    def __str__(self):
        return self.info.Bakery_name


class Bakery_Review(models.Model):
    info = models.ForeignKey(Bakery_Info, on_delete=models.CASCADE)
    Bakery_Reviewer = models.CharField(max_length=50)
    Bakery_Contents = models.TextField()

    def __str__(self):
        return self.info.Bakery_name