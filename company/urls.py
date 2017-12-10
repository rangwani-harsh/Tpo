from django.conf.urls import url,include
from . import views

urlpatterns = [
    
    #url(r'^login/',views.studentLogin,name = 'comptLogin'),
    url(r'^signup/',views.companySignUp,name = 'companySignUp'),
    url(r'^dashboard/(\d*)$',views.companyDashboard,name = 'companyDashboard'),
    url(r'^dashboard/$',views.companyDashboard,name = 'companyDashboard'),
    #url(r'acadview/',views.studentAcademicDetail,name='studentAcademicDetail'),
    
]