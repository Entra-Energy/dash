from django.urls import path,re_path
from dash_back.views import PostView,OnlineView
#from dash_back import views
app_name = "posts"


urlpatterns = [
    re_path('^posts/$', PostView.as_view()),
    #path(r'^posts$',PostView.as_view()),
    path('online/', OnlineView.as_view()),
]
