# from django.urls import path,re_path
# from dash_back.views import PostView,OnlineView
#from dash_back import views
from rest_framework.routers import DefaultRouter
from dash_back import views
from django.urls import path


app_name = "dash_back"
router = DefaultRouter()
#
router.register(r'posts', views.PostViewset, basename='posts')
router.register(r'price', views.PriceViewset, basename='price')

urlpatterns = [
    path('online/', views.OnlineView.as_view(), name = 'test'),
    path('correction/', views.post_data, name='post_val'),
    path('cali/',views.post_cali, name='cali'),
    path('single-corr/',views.post_single_correction, name='single_corr'),
    path('reset/',views.reset_data, name='reset'),
    path('flexi/',views.flexi_send, name='flexi'),
]

urlpatterns += router.urls
