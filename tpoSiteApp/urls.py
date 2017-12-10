from django.conf.urls import url,include
from . import views

urlpatterns = [
    
    #url(r'^login/',views.studentLogin,name = 'Login'),
    url(r'^signup/',views.studentSignUp,name = 'studentSignUp'),
    url(r'acadview/',views.studentAcademicDetail,name='studentAcademicDetail'),
    url(r'^dashboard/',views.studentDashboard,name = 'studentDashboard'),
    url(r'^policies/',views.policies,name = 'policies'),
    
]