from django.urls import path
from blog import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    path('home',views.home,name="home"),
    path('register',views.register),
    path('test',views.Test,name="Test"),
    path('Test_in_development_mode',views.Test_in_development_mode,name="Test_in_development_mode"),
    path('rulesofexam',views.rulesofexam,name="rulesofexam"),
    
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
