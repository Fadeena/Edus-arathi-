"""
URL configuration for edu_saradhi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homefun,name='home'),
    path('login/',loginfun, name='login'),
    path('register/',registerfun, name='register'),
    path('adminhome/',adminfun,name='admin'),
    path('tutorhome/',tutorfun,name='tutor'),
    path('student/',studentfun,name='student'),
    path('aduserlist/',userlistfun,name='userlist'),
    path('adapproveuser/<int:uid>/',approveuserfun,name='approveuser'),
    path('pendinguser/',pendinguserfun,name='pendinguser'),
    path('adaddcourse/',addcoursefun,name='addcourse'),
    path('viewcourses/',viewcoursefun,name='viewcourses'),
    path('userdetail/<int:u_id>/',userdetailfun,name='userdetail'),


    path('explorecourses/',explorecoursesfun,name='explorecourses'),
    path('aboutus/',aboutusfun,name='aboutus'),
    path('contactus/',contactusfun, name='contactus'),


    path('mycourse/',mycoursefun,name='mycourse'),
    path('materialupload/',uploadfun,name='materialupload'),
    path('uploadlist/',uploadlistfun,name='uploadlist'),
    path('aipromptlab/',aipromptlabfun,name='aipromptlab'),
    path('quizgenerator/',quizgeneratorfun,name='quizgenerate'),
    path('studentlist/',studentlistfun,name='studentlist'),
    path('tuviewdetail/<int:u_id>/',tuviewdetailfun,name='tuviewdetail'),


    path('choosecourse/',choosecoursefun,name='choosecourse'),
    path('mystudyplan/',studyplanfun,name='mystudyplan'),
    path('aitutorchat',aitutorchatfun,name='aitutorchat'),
    path('activecourses/',activecoursesfun,name='activecourses'),
    path('quiz/',quizfun,name='quiz'),
    path('viewquiz/',viewquizfun,name='viewquiz'),
    path('library/',libraryfun,name='library'),
    path('chatselect/',chatselectfun, name='chatselect'),
    path('studentchat/<int:tutor_id>/',studentchatfun, name="studentchat"),
    path('tutorchat/',tutorchatfun,name="tutorchat"),
    path('reply/<int:chat_id>/',replyfun, name="reply"),
    
    path('logout/',logoutfun),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
