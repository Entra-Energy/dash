from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from dash_back.serializers import PostSerializer, OnlineSerializer, PriceSerializer
from dash_back.models import Post, Online, Price
from datetime import datetime
from dash_back.custom_filters import PostFilter, PriceFilter


# class PostView(APIView):
#     # def get(self, request):
#     #     range = self.request.GET.get('range')
#     #     if range == '0':
#     #         posts = Post.today.all()
#     #     else:
#     #         posts = Post.month.all()
#     serializer = PostSerializer(posts, many=True)
#     # return Response({"posts": serializer.data})
class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_class = PostFilter


class  OnlineView(APIView):
    def get(self, request):
        online = Online.dist.all()

        serializer = OnlineSerializer(online, many=True)
        return Response({"online": serializer.data})


class PriceViewset(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_class = PriceFilter


# def help_price(request):
#     #test = request.GET.get('dashboard', '')
#     print("sdfhhhh")
#     return HttpResponse("OK")
