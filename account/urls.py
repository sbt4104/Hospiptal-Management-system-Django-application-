from django.conf.urls import url
from account import views

# SET THE NAMESPACE!
app_name = 'basic_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^register2/$',views.register2,name='register2'),
    url(r'^user_login2/$',views.user_login2,name='user_login2'),    
    url(r'^schedules1/$',views.schedules1,name='schedules1'),
    url(r'^schedules2/$',views.schedules2,name='schedules2'),
    url(r'^appointment/$',views.appointment,name='appointment'),
    url(r'^appointdoc/$',views.appointdoc,name='appointdoc'),
    url(r'^doctoform/$',views.doctoform,name='doctoform'),        
    url(r'^selectdoctor/(?P<pk>\d+)/$',views.selectdoctor,name='selectdoctor'),    
    url(r'^deletesc/(?P<pk>\d+)/$',views.deletesc,name='deletesc'),        
    url(r'^updatestatus1/(?P<pk>\d+)/$',views.updatestatus1,name='updatestatus1'),        
    url(r'^updatestatus2/(?P<pk>\d+)/$',views.updatestatus2,name='updatestatus2'),
    url(r'^showall1/$',views.show_all1,name='showall1'),        
    url(r'^showall2/$',views.show_all2,name='showall2'),
    url(r'^downloadpdf/(?P<pk>\d+)/$',views.downloadpdf,name='downloadpdf'),                                   
    url(r'^upload/$', views.upload_csv, name='upload_csv'), 
    url(r'^searchfield/$',views.searchfield,name='searchfield'),
]