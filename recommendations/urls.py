from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/recommend/', views.get_recommendation_ajax, name='recommend_ajax'),
    path('api/email/',views.email_recommendations, name='email_recommendations'),
    path('api/summary/', views.get_summary, name='get_summary'),
    path('api/emailSum/',views.email_summary, name='email_summary'),
    path('api/emailNotif/',views.send_notif, name='send_notif'),

]