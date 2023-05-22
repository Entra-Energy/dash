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
router.register(r'aris', views.ArisViewset, basename='aris')
router.register(r'price', views.PriceViewset, basename='price')
router.register(r'flexi_res', views.FlexiViewset, basename='flexi_res')
router.register(r'userip', views.userIpViewset, basename='userip')
# router.register(r'post_forecast', views.PostForecastViewset, basename='postForecast')
router.register(r'flexi_sim', views.SimLogViewset, basename='sim_log')
router.register(r'grid_asign', views.GridViewset, basename='gridset')
router.register(r'capa_asign', views.CapaViewset, basename='capaasign')

urlpatterns = [
    path('online/', views.OnlineView.as_view(), name = 'test'),
    path('correction/', views.post_data, name='post_val'),
    path('cali/',views.post_cali, name='cali'),
    path('single-corr/',views.post_single_correction, name='single_corr'),
    path('reset/',views.reset_data, name='reset'),
    path('flexi/',views.flexi_send, name='flexi'),
    path('login-data/',views.login_data, name='login_data'),
    path('sched/',views.sched_flexi, name='sched_flexi'),
    path('execall/',views.exec_all, name='exec_all'),
    path('asign/',views.asign_node, name='asign'),
    path('capa/',views.asign_capa, name='capa'),
    
]

urlpatterns += router.urls
