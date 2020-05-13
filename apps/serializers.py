from rest_framework import serializers,exceptions
from apps.models import Employee
from day01 import settings

#为每一个model类都要编写一个独立的序列化器
class EmployeeModelSerializer(serializers.Serializer):
    #数据库里面的字段
    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.CharField()
    pic = serializers.ImageField()
    #自定义一个序列化字段
    address = serializers.SerializerMethodField()
    def get_address(self,obj):
        return "China"

    #对数据库中已存在的字段进行处理
    #返回性别而非直接返回0，1
    gender = serializers.SerializerMethodField()
    def get_gender(self,obj):
        # 如果获取choices类型解释型的值，可以通过 get_字段名_display()访问
        return obj.get_gender_display()
    #自定义返回图片的全路径
    def get_pic(self,obj):
        print(settings.MEDIA_URL)
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, str(obj.pic))


#反序列化
class EmployeeModelDeserializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=8,
        min_length=3,
        error_messages={
            "max_length": "用户名长度不能超过8位",
            "min_length": "用户名长度不能低于3位"
        }
    )
    password = serializers.CharField()
    # 写在反序列化里面的时必填项，如果不想是必填项，对required设置false
    phone = serializers.CharField(required=False)

    # 重复密码
    re_pwd = serializers.CharField()

    # 局部校验钩子 对反序列化器中的某个字段进行校验
    def validate_username(self, value):
        if "1" in value:
            raise exceptions.ValidationError("用户名异常")
        return value

    # 全局的校验钩子，会对反序列化器中所有校验规则进行验证
    def validate(self, attrs):
        print(attrs, "attr")
        password = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        if password != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")
        return attrs

    # 完成员工新增需要实现create方法
    # 在create()方法完成保存之前  会先调用局部钩子  全局钩子函数来完成字段的校验
    def create(self, validated_data):
        print(validated_data)
        # 自己实现保存的逻辑 校验数据 校验通过后保存
        return Employee.objects.create(**validated_data)
