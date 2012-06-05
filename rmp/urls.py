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
	
	# Ratings
	url(r'^$', 'rating.views.index'),
	
	url(r'^ppt/random$', 'rating.views.gotorandom'),
	#url(r'^ppt/(?P<ppt_id>\d+)\$', 'rating.views.view'),
	url(r'^ppt/(?P<ppt_id>\d+)/rate$', 'rating.views.rate'),
	url(r'^ppt/(?P<folder>\d+)/jpg/(?P<filename>\w+)\.JPG$', 'rating.views.jpg'),
)
