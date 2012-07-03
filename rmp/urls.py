from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	url(r'^admin/', include(admin.site.urls)),
	
	# Login/out
	url(r'^accounts/login', 'django.contrib.auth.views.login'),
	url(r'^accounts/logout', 'django.contrib.auth.views.logout'),
	#url(r'^registration/password_change', 'django.contrib.auth.views.password_change'),
	#url(r'^registration/password_reset', 'django.contrib.auth.views.password_reset'),

)

urlpatterns += patterns('rating.views',
	
	# Homepage
	url(r'^$', 'homepage'),
	
	# Rating
	url(r'^ppt/random$', 'goto_random'),
	
	# User Ppts
	url(r'^user/$', 'user_list'),
	url(r'^user/(?P<username>\w+)/$', 'user_view'),
	url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/$', 'user_ppt_view'),
	url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/metadata$', 'user_ppt_view_metadata'),
	
	url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/rate$', 'user_ppt_rate'),
	url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/jpg/Slide(?P<slide>\d+)\.JPG$', 'user_ppt_jpg'),
	
	## View the exported html.htm file and other image files
	url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/html.htm$', 'user_ppt_htm'),
	url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/html_files/(?P<filename>.*)$', 'user_ppt_img'),
	url(r'^user/(?P<username>\w+)/ppt/(?P<ppt_id>\d+)/img/(?P<filename>.*)$', 'user_ppt_img'),
	
	# Create
	url(r'^user/(?P<username>\w+)/ppt/upload$', 'user_ppt_upload'),
	

	### Units
	url(r'^unit/(?P<unit_id>\w+)/$', 'unit_view'),


	### Tags
	url(r'^tag/(?P<tag>\w+)/$', 'tag_view'),
	
	
	# Images (OLD FASHION)
	url(r'^ppt/(?P<folder>\d+)/jpg/(?P<filename>\w+)\.JPG$', 'ppt_jpg'),
)
