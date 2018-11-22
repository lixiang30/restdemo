from django.shortcuts import render,HttpResponse

# Create your views here.
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView
from app01.serializer import *
from app01.utils import SVIPPermission

class PublishView(APIView):
    def get(self,request):
        publish_list = Publish.objects.all()
        ps = PublishModelSerializers(publish_list,many=True)
        return Response(ps.data)
    def post(self,request):
        ps = PublishModelSerializers(data=request.data)
        if ps.is_valid():
            ps.save()
            return Response(ps.data)
        else:
            return Response(ps.errors)

class PublishDetaiView(APIView):
    def get(self,request,pk):
        book = Publish.objects.filter(pk=pk).first()
        bs = PublishModelSerializers(book)
        return Response(bs.data)

    def put(self,request,pk):
        book = Publish.objects.filter(pk=pk).first()
        bs = PublishModelSerializers(book,data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)
    def delete(self,request,pk):
        book = Publish.objects.filter(pk=pk).delete()
        return Response()

from rest_framework import exceptions
#认证
class TokenAuth(object):
    def authenticate(self,request):
        token = request.GET.get("token")
        token_obj = Token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("验证失败")
        else:
            return token_obj.user.name,token_obj.token  # 返回一个元组
    def authenticate_header(self,request):
        pass

# ++++++++++++++++++++++++++++++++++++++++++++++++++分页+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
class MyPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 3

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1


class BookView(APIView):
    # 认证
    # authentication_classes = [TokenAuth,]
    # 权限
    # permission_classes = [SVIPPermission,]
    # 频率
    # throttle_classes = []

    def get(self,request):
        book_list = Book.objects.all()

        # 分页
        # pnp = MyPageNumberPagination()
        pnp = MyLimitOffsetPagination()
        books_page = pnp.paginate_queryset(book_list,request,self)

        ps = BookModelSerializers(books_page,many=True,context={"request":request})
        return Response(ps.data)
    def post(self,request):
        ps = BookModelSerializers(data=request.data)
        if ps.is_valid():
            ps.save()
            return Response(ps.data)
        else:
            return Response(ps.errors)


class BookDetailView(APIView):
    def get(self,request,pk):
        book = Book.objects.filter(pk=pk).first()
        bs = BookModelSerializers(book,context={"request":request})
        return Response(bs.data)

    def put(self,request,pk):
        book = Book.objects.filter(pk=pk).first()
        bs = BookModelSerializers(book,data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)
    def delete(self,request,pk):
        book = Book.objects.filter(pk=pk).delete()
        return Response()

# ==========================================================mixins类===================================================
# from rest_framework import mixins
# from rest_framework import generics
# class AuthorView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorModelSerializers
#
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
#
# class AuthorDetailView(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,generics.GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorModelSerializers
#
#     def get(self, request,*args, **kwargs):
#         return self.retrieve(request,*args, **kwargs)
#
#     def delete(self, request,*args, **kwargs):
#         return self.destroy(request,*args, **kwargs)
#
#     def put(self, request,*args, **kwargs):
#         return self.update(request,*args, **kwargs)

#  =================================================基于类的通用视图======================================================
# from rest_framework import mixins
# from rest_framework import generics
# class AuthorView(generics.ListCreateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorModelSerializers
#
# class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorModelSerializers

from rest_framework.response import Response


from rest_framework import viewsets
class AuthorModelView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializers
    pagination_class = MyPageNumberPagination

# =====================================================认证==============================================================

def get_random_str(user):
    import hashlib,time
    ctime = str(time.time())
    md5 = hashlib.md5(bytes(user,encoding="utf-8"))
    md5.update(bytes(ctime,encoding="utf-8"))
    return md5.hexdigest()

class LoginView(APIView):
    def post(self,request):
        name = request.data.get("name")
        pwd = request.data.get("pwd")
        user = User.objects.filter(name=name,pwd=pwd).first()
        res = {"state_code":1000,"msg":None}
        if user:
            random_str = get_random_str(user.name)
            token = Token.objects.update_or_create(user=user,defaults={"token":random_str})
            res["token"] = str(token)
        else:
            res["token"] = 1001 # 错误的状态码
            res["msg"] = "用户名或者密码错误"
        import json
        return Response(json.dumps(res))

from rest_framework.parsers import JSONParser,FormParser
class PaserView(APIView):
    parser_classes = [JSONParser,FormParser]
    # JSONParser:表示只能解析content-type:application/json的头
    # FormParser:表示只能解析content-type:application/x-www-form-urlencoded的头

    def post(self,request,*args,**kwargs):
        # 获取解析的结果
        print(request.data)
        return HttpResponse('parser')
