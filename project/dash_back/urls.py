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

urlpatterns = router.urls

# urlpatterns = [
#     re_path('^posts/$', PostView.as_view()),
#     #path(r'^posts$',PostView.as_view()),
#     path('online/', OnlineView.as_view()),
# ]
