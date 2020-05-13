from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from apps.models import UserInfo, Student, Employee
from apps.serializers import EmployeeModelSerializer, EmployeeModelDeserializer


def index(request):
    return HttpResponse("测试一下路径是否可用")
@method_decorator(csrf_exempt,name="dispatch")
class UserView(View):
    #get请求，查询单个用户和查询所有用户信息
    def get(self,request,*args,**kwargs):
        user_id = kwargs.get('pk')
        #查询单个用户
        if user_id:
            #如果id存在查询单个用户信息，如果所加id在数据库中没有，获取用户信息失败
            user_value = UserInfo.objects.filter(pk=user_id).values("username","password","gender").first()
            if user_value:
                return JsonResponse({
                    "status":200,
                    "message":"单个用户信息获取成功",
                    "results":user_value
                })
        else:
            #如果在路径后面没有加id则查询所有用户
            user_list = UserInfo.objects.all().values("username","password","gender")
            if user_list:
                return JsonResponse({
                    "status":201,
                    "message":"获取用户列表信息成功",
                    "result":list(user_list)
                })
            #if-else语句都不对，执行此处的return
        return JsonResponse({
            "status":500,
            "message":"获取用户信息失败"
        })
    #post请求添加用户
    def post(self,request,*args,**kwargs):
        print(request.POST)
        try:
            #将用户信息添加到数据库
            user_obj = UserInfo.objects.create(**request.POST.dict())
            if user_obj:
                return JsonResponse({
                    "status":200,
                    "message":"添加用户成功",
                    "results":{"username":user_obj.username,"gender":user_obj.gender}
                })
            else:
                return JsonResponse({
                    "status":500,
                    "message":"添加用户失败"
                })
        except:
            #try中语句未执行，则执行此处的except异常
            return JsonResponse({
                "status":501,
                "message":"参数有误"
            })
    #put请求修改用户信息
    def put(self,request,*args,**kwargs):
        username = request.username,
        password = request.password,
        gender = request.gender
        user_id = kwargs.get("pk")
        user = UserInfo.objects.filter(pk=user_id).first()
        if user:
            user_obj = UserInfo.objects.create(username=username,password=password,gender=gender)
            if user_obj:
                return JsonResponse({
                    "status":200,
                    "message":"修改用户信息成功",
                    "results":{"username":user_obj.username,"password":user_obj.password,"gender":user_obj.gender}
                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "修改用户信息失败"
                })
        else:
            return JsonResponse({
                "status":500,
                "message":"修改用户信息失败"
            })

    #delete请求，删除用户信息
    def delete(self,request,*args,**kwargs):
        user_id = kwargs.get("pk")
        if user_id:
            user = UserInfo.objects.filter(pk=user_id).delete()
            return JsonResponse({
                "status":200,
                "message":"删除用户成功"
            })
        else:
            return JsonResponse({
                "status":500,
                "message":"删除用户信息失败"
            })

class StudentView(APIView):
    def get(self,request,*args,**kwargs):
        #获取学生信息id
        stu_id = kwargs.get("pk")
        #如果id存在查询单个信息
        if stu_id:
            stu_value = Student.objects.filter(pk=stu_id).values("name","sex").first()
            if stu_value:
                return Response({
                    "status": 200,
                    "message": "学生信息获取成功",
                    "results": stu_value #返回单个学生信息
                })
        else:
            stu_list = Student.objects.filter(pk=stu_id).values("name", "sex")
            if stu_list:
                return Response({
                    "status": 201,
                    "message": "获取学生列表信息成功",
                    "result": list(stu_list)
                })
        return Response({
            "status": 500,
            "message": "获取学生信息失败"
        })

    def post(self,request,*args,**kwargs):
        try:
            stu_obj = Student.objects.create(**request.data.dict())
            if stu_obj:
                return Response({
                    "status": 200,
                    "message": "添加学生成功",
                    "results": {"name": stu_obj.name, "sex": stu_obj.sex}
                })
            else:
                return Response({
                    "status": 500,
                    "message": "添加学生失败"
                })
        except:
            return Response({
                "status": 501,
                "message": "参数有误"
            })


class EmployeeAPIView(APIView):
    #get方法查询：从数据库中取到前台-->对数据进行序列化
    def get(self,request,*args,**kwargs):
        emp_id = kwargs.get("id")
        if emp_id:
            try:
                emp_obj = Employee.objects.get(pk=emp_id)
                #序列化
                emp_ser = EmployeeModelSerializer(emp_obj).data
                return Response({
                    "status":200,
                    "message":"查询单个员工信息",
                    "results":emp_ser,
                })
            except:
                return Response({
                    "status":500,
                    "message":"用户不存在"
                })
        else:
            emp_list = Employee.objects.all()
            emp_ser = EmployeeModelSerializer(emp_list,many=True).data
            return Response({
                "status":200,
                "message":"查询员工列表信息成功",
                "results":emp_ser,
            })

    def post(self,request,*args,**kwargs):
        request_data = request.data
        if not isinstance(request_data,dict) or request_data == {}:
            return Response({
                "status":500,
                "message":"数据有误"
            })
        deserializer = EmployeeModelDeserializer(data=request_data)
        if deserializer.is_valid():
            emp_obj = deserializer.save()
            return Response({
                "status":200,
                "message":"员工信息添加成功",
                "results":EmployeeModelSerializer(emp_obj).data
            })
        else:
            return Response({
                "status":500,
                "message":"员工信息添加失败",
                "results":deserializer.errors
            })



