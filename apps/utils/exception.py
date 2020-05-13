from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

def exception_handler(exc,context):
    response = drf_exception_handler(exc,context)
    #打印错误的详细信息，在后台显示
    error = "%s %s %s" % (context['view'],context['request'].method,exc)
    print(error)
    if response is None:
        return Response(
            {"error":"中断异常，请检查错误"},status=status.HTTP_500_INTERNAL_SERVER_ERROR,exception=None
        )
    return response