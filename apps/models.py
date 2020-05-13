from django.db import models

# Create your models here.
class UserInfo(models.Model):
    gender_choices = (
        (0,'female'),
        (1,'male'),
        (2,'unknown'),
    )
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30,blank=True,null=True)
    gender = models.SmallIntegerField(choices=gender_choices,default=1)
    class Meta:
        db_table = "tb_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class Student(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField
    sex = models.BooleanField(default=1)
    class Meta:
        db_table="tb_student"
        verbose_name="学生"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Employee(models.Model):
    gender_choices = (
        (0, 'female'),
        (1, 'male'),
        (2, 'unknown'),
    )
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30, blank=True, null=True)
    gender = models.SmallIntegerField(choices=gender_choices, default=1)
    phone = models.CharField(max_length=11)
    pic = models.ImageField(upload_to="pic",default="pic/1.jpg")
    class Meta:
        db_table = "tb_employee"
        verbose_name = "员工"
        verbose_name_plural = verbose_name