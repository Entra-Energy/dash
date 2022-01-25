from django.shortcuts import render

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from dash_back.serializers import PostSerializer, OnlineSerializer
from dash_back.models import Post, Online
from datetime import datetime


class PostView(APIView):
    def get(self, request):
        range = self.request.GET.get('range')
        if range == '0':
            posts = Post.today.all()
        else:
            posts = Post.month.all()
        serializer = PostSerializer(posts, many=True)
        return Response({"posts": serializer.data})



class  OnlineView(APIView):
    def get(self, request):
        online = Online.dist.all()

        serializer = OnlineSerializer(online, many=True)
        return Response({"online": serializer.data})
