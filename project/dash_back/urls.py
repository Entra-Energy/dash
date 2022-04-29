# from django.urls import path,re_path
# from dash_back.views import PostView,OnlineView
#from dash_back import views
from rest_framework.routers import DefaultRouter
from dash_back import views
from django.urls import path


app_name = "dash_back"
router = DefaultRouter()

router.register(r'posts', views.PostViewset, basename='posts')
router.register(r'price', views.PriceViewset, basename='price')



urlpatterns = [
    path('dashboard/', views.help_price,),
]
urlpatterns += router.urls
