from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from .models import *
from rest_framework.views import APIView
from app01.serializer import *

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
    def get(self,request,id):
        book = Publish.objects.filter(pk=id).first()
        bs = PublishModelSerializers(book)
        return Response(bs.data)

    def put(self,request,id):
        book = Publish.objects.filter(pk=id).first()
        bs = PublishModelSerializers(book,data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)
    def delete(self,request,id):
        book = Publish.objects.filter(pk=id).delete()
        return Response()


class BookView(APIView):
    def get(self,request):
        book_list = Book.objects.all()
        ps = BookModelSerializers(book_list,many=True)
        return Response(ps.data)
    def post(self,request):
        ps = BookModelSerializers(data=request.data)
        if ps.is_valid():
            ps.save()
            return Response(ps.data)
        else:
            return Response(ps.errors)


class BookDetailView(APIView):
    def get(self,request,id):
        book = Book.objects.filter(pk=id).first()
        bs = BookModelSerializers(book)
        return Response(bs.data)

    def put(self,request,id):
        book = Book.objects.filter(pk=id).first()
        bs = BookModelSerializers(book,data=request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)
    def delete(self,request,id):
        book = Book.objects.filter(pk=id).delete()
        return Response()
