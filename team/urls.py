from django.conf.urls import url,include
from . import views

urlpatterns = [
    
    #url(r'^login/',views.studentLogin,name = 'comptLogin'),
    #url(r'^signup/',views.companySignUp,name = 'companySignUp'),
    url(r'^notificationgen/',views.generateNotification,name = 'generateNotification'),
    url(r'^servicegen/',views.generateService,name = 'generateService'),
    url(r'^verifywillingness/',views.verifyWillingness,name = 'verifyWillingness'),
    url(r'^verifyacad',views.verifyAcademicDetail,name = 'verifyAcademicDetail'),
    url(r'^viewstudents',views.viewStudents,name = 'viewStudents'),
    url(r'^viewCompanies',views.companyView,name = 'companyView'),
    url(r'^viewmembers',views.viewMembers,name = 'viewMembers'),
    url(r'^viewslots',views.slotDefine,name = 'slotDefine'),
    url(r'^adminview/$',views.adminView,name = 'adminView'),
    url(r'^willingness/$',views.willingnessAdmin,name = 'willingnessAdmin'),
    #url(r'acadview/',views.studentAcademicDetail,name='studentAcademicDetail'),
    
]