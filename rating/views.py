# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings

import os

from rating.models import *
from rating.forms import *



@login_required
def index(request):
	user = request.user
	
	ratings = PptRating.objects.filter(user__username=user).order_by('-ratedate')
	
	return render_to_response('rating/index.html', 
			{	'username': user.username,
				'count': ratings.count(),
				'ratings': ratings.all()
			},
			context_instance=RequestContext(request))


@login_required
def gotorandom(request):
	
	ppt_list = Ppt.objects.filter(user__username = 'pearson')
	ppt_list = ppt_list.exclude(pptrating__user__username=request.user.username)
	ppt_list = ppt_list.order_by('rnd')[:1]
	
	if len(ppt_list) == 0:
		return HttpResponse('No more Ppt to rate')
	else:
		ppt_list = ppt_list[0]
	
	return HttpResponseRedirect('/ppt/'+str(ppt_list.pk)+'/rate')



@login_required
def view(request, ppt_id):
	ppt = get_object_or_404(Ppt, pk=ppt_id)
	
	# If me, then show all ratings.  Otherwise, shown own ratings.
	if request.user.username == 'garrettn':
		ratings = PptRating.objects.filter(ppt_id=ppt.id)
	else:
		ratings = PptRating.objects.filter(ppt_id=ppt.id).filter(user__username=request.user.username)
	
	# refactor out jpg access
	jpg = settings.PPT_FILEPATH + ppt.folder + '/jpg/'
	if not os.path.exists(jpg):
		return HttpResponse('No images for given ppt in ' + jpg)
	
	jpgs = []
	for j in os.listdir(jpg):
		if j[-3:] == 'JPG': jpgs.append('/ppt/'+ppt.folder+'/jpg/'+j)
	
	return render_to_response('rating/view.html', 
			{	'username': request.user.username,
				'jpgs': jpgs,
				'ppt': ppt,
				'ratings': ratings.all()
			},
			context_instance=RequestContext(request))


@login_required
def rate(request, ppt_id):
	ppt = get_object_or_404(Ppt, pk=ppt_id)
	
	if request.method == 'POST':
		form = PptRatingForm(request.POST)
		if form.is_valid():
			
			new_rating = form.save(commit=False)
			new_rating.user = request.user
			new_rating.ppt = ppt
			new_rating.save()
			form.save_m2m()
			return HttpResponseRedirect('/')
	else:
		
		# refactor out jpg access
		jpg = settings.PPT_FILEPATH + ppt.folder + '/jpg/'
		if not os.path.exists(jpg):
			return HttpResponse('No images for given ppt in ' + jpg)
		
		jpgs = []
		for j in os.listdir(jpg):
			if j[-3:] == 'JPG': jpgs.append('/ppt/'+ppt.folder+'/jpg/'+j)
		
		form = PptRatingForm()
	
	return render_to_response('rating/rate.html',
			{ 'ppt': ppt, 'jpgs': jpgs, 'form':form },
			context_instance=RequestContext(request))


# Return a jpg image.
@login_required
def jpg(request, folder, filename):
	if '..' in folder or '..' in filename:
		raise Http404
	
	filepath = settings.PPT_FILEPATH + folder + '/jpg/'+filename + '.JPG'
	
	try:
		f = open(filepath, 'rb')
		return HttpResponse(f.read())
	except:
		raise Http404



