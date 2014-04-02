from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


# Admin Patterns.
urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout'),
    #url(r'^registration/password_change', 'django.contrib.auth.views.password_change'),
    #url(r'^registration/password_reset', 'django.contrib.auth.views.password_reset'),
)



## Core PPT uploading and management.
urlpatterns += patterns('ppt.views',
    url(r'^$', 'homepage'),
    
    ## User 
    url(r'^user/$', 'user_list'),
    url(r'^accounts/profile/$', 'user_view'), # current user shortcut from accounts/login
    url(r'^user/(?P<username>\w+)/$', 'user_view'),

    # PPT
    url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/$', 'user_ppt_view'),
    url(r'^user/(?P<username>\w+)/ppt/upload$', 'user_ppt_edit'),
    url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/edit$', 'user_ppt_edit'),
    
    # Unit    
    url(r'^unit/$', 'unit_list'),
    url(r'^unit/(?P<unit_id>\w+)/$', 'unit_view'),
)

## Survey for 2014 Summer Experiment
urlpatterns += patterns('exp1.views',
    url(r'^experiment/pre$', 'ppt_survey_pre'),
    url(r'^experiment/(?P<experiment>\w)/(?P<ppt_id>\d+)/video1$', 'ppt_survey_video1'),
    url(r'^experiment/(?P<experiment>\w)/(?P<ppt_id>\d+)/video2$', 'ppt_survey_video2'),
    url(r'^experiment/thanks.html$', 'ppt_survey_post'),
)

## Static file patterns.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

## Media
from django.conf.urls.static import static
from rmp.local_settings import MEDIA_URL, MEDIA_ROOT

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)