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
import random

from rating.models import *
from rating.forms import *
from rating.parser import HtmlParser


@login_required
def homepage(request):
	user = request.user
	
	ratings = PptRating.objects.filter(user__username=user).order_by('-ratedate')
	
	return render_to_response('rating/index.html', 
			{	'username': user.username,
				'count': ratings.count(),
				'ratings': ratings.all()
			},
			context_instance=RequestContext(request))



@login_required
def goto_random(request):
	
	ppt_list = Ppt.objects.filter(user__username = 'pearson')
	ppt_list = ppt_list.exclude(pptrating__user__username=request.user.username)
	ppt_list = ppt_list.order_by('rnd')[:1]
	
	if len(ppt_list) == 0:
		return HttpResponse('No more Ppt to rate')
	else:
		ppt_list = ppt_list[0]
		user = ppt_list.user
	
	return HttpResponseRedirect('/user/%s/ppt/%s/rate' % (user.username, ppt_list.pk))



@login_required
def user_view(request, username):
	user = get_object_or_404(User, username=username)
	
	ppts = Ppt.objects.filter(user_id=user.id).order_by('pk')
	
	return render_to_response('rating/user_view.html',
			{	'user': user,
				'ppts': ppts
			},
			context_instance=RequestContext(request)
	)



@login_required
def user_ppt_view(request, username, ppt_id):
	user = get_object_or_404(User, username=username)
	ppt = Ppt.objects.get(user_id=user.id, id=ppt_id)
	
	ratings = PptRating.objects.filter(ppt_id=ppt_id)
	pptuploadedfiles = PptUploadedFile.objects.filter(ppt_id=ppt_id)
	jpgs = ppt.jpgs()
	
	return render_to_response('rating/user_ppt_view.html',
			{	'user': user,
				'ppt': ppt,
				'jpgs': jpgs,
				'ratings': ratings,
				'pptuploadedfiles': pptuploadedfiles
			},
			context_instance=RequestContext(request)
	)



@login_required
def user_ppt_view_metadata(request, username, ppt_id):
	user = get_object_or_404(User, username=username)
	ppt = Ppt.objects.get(user_id=user.id, id=ppt_id)
	
	ratings = PptRating.objects.filter(ppt_id=ppt_id)
	pptuploadedfiles = PptUploadedFile.objects.filter(ppt_id=ppt_id)
	jpgs = ppt.jpgs()
	
	# Make sure that we have parsed the file...
	filepath  = '%suserfiles/pptfile/%s/%s/' % (settings.PPT_FILEPATH, user.id, ppt_id)
	#parser = HtmlParser(ppt, filepath, True)
	
	pptHtmlImages = PptHtmlImage.objects.filter(ppt_id=ppt_id)
	pptHtmlPages = PptHtmlPage.objects.filter(ppt_id=ppt_id)
	
	for p in pptHtmlPages:
		filename = 'Slide%s.JPG' % p.order()
		p.jpgs = PptJpg.objects.filter(ppt_id=ppt_id,filename=filename)
	
	return render_to_response('rating/user_ppt_view_metadata.html',
			{	'user': user,
				'ppt': ppt,
				'pptHtmlPages': pptHtmlPages,
			},
			context_instance=RequestContext(request)
	)


# Return a html file index.
@login_required
def user_ppt_htm(request, username, ppt_id):
	user = get_object_or_404(User, username=username)
	
	filepath  = '%suserfiles/pptfile/%s/%s/html.htm' % (settings.PPT_FILEPATH, user.id, ppt_id )
	try:
		f = open(filepath, 'rb')
		return HttpResponse(f.read())
	except:
		raise Http404



# Return a jpg image.
@login_required
def user_ppt_jpg(request, username, ppt_id, slide):
	user = get_object_or_404(User, username=username)
	
	filepath  = '%suserfiles/pptfile/%s/%s/jpg/Slide%s.JPG' % (settings.PPT_FILEPATH, user.id, ppt_id, slide )
	try:
		f = open(filepath, 'rb')
		return HttpResponse(f.read())
	except:
		raise Http404


# Return an image that was exported from a html presentation
@login_required
def user_ppt_img(request, username, ppt_id, filename):
	user = get_object_or_404(User, username=username)
	if '..' in filename:
		raise Http404
	
	filepath  = '%suserfiles/pptfile/%s/%s/html_files/%s' % (settings.PPT_FILEPATH, user.id, ppt_id, filename )
	try:
		f = open(filepath, 'rb')
		return HttpResponse(f.read())
	except:
		raise Http404


@login_required
def XXXXuser_ppt_view(request, username, ppt_id):
	ppt = get_object_or_404(Ppt, pk=ppt_id)
	
	# If me, then show all ratings.  Otherwise, shown own ratings.
	if request.user.username == 'garrettn':
		ratings = PptRating.objects.filter(ppt_id=ppt.id)
	else:
		ratings = PptRating.objects.filter(ppt_id=ppt.id).filter(user__username=request.user.username)
	
	# refactor out jpg access
	jpg = settings.PPT_FILEPATH + ppt.folder + '/jpg/'
	if not os.path.exists(jpg):
		return HttpResponse('No images for this presentation')
	
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
def user_ppt_upload(request, username):
	
	if request.method == 'POST':
		
		pptForm = PptForm(request.POST)
		pptUploadedFileForm = PptUploadedFileForm(request.POST, request.FILES)
		
		if pptForm.is_valid() and pptUploadedFileForm.is_valid():
			
			# Save Ppt record
			ppt = pptForm.save(commit=False)
			ppt.user = request.user
			ppt.folder = ''
			ppt.filename = ''
			ppt.rnd = random.randint(0, 1000000000)
			ppt.unit_id = 0 
			ppt.save()
			pptForm.save_m2m()
			
			# Save actual uploaded file
			pptUploadedFile = pptUploadedFileForm.save(commit=False)
			pptUploadedFile.ppt = ppt
			pptUploadedFile.save()
			pptUploadedFileForm.save_m2m()
			
			return HttpResponseRedirect('/ppt/%s' % (ppt.id))
		
	else:
		pptForm = PptForm()
		pptUploadedFileForm = PptUploadedFileForm()
	
	return render_to_response('rating/upload.html', 
			{	'pptForm': pptForm, 
				'pptUploadedFileForm': pptUploadedFileForm
			},
			context_instance=RequestContext(request)
	)


#@login_required
#def viewUserPpt(self):
	



@login_required
def user_ppt_rate(request, username, ppt_id):
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
			p = PptRating()
			p.user_id = request.user.id
			p.ppt_id = ppt_id
			p.empty = 1
			p.contentimage = 0
			p.contenttext = 0
			p.slidenovel = 0
			p.slidestudy = 0
			p.slidequality = 0
			p.slideinteresting = 0
			
			p.save()
			return HttpResponseRedirect('/ppt/random')
		
		jpgs = []
		for j in os.listdir(jpg):
			if j[-3:] == 'JPG': jpgs.append('/ppt/'+ppt.folder+'/jpg/'+j)
		
		form = PptRatingForm()
	
	return render_to_response('rating/rate.html',
			{ 'ppt': ppt, 'jpgs': jpgs, 'form':form },
			context_instance=RequestContext(request))


# Return a jpg image.
@login_required
def ppt_jpg(request, folder, filename):
	if '..' in folder or '..' in filename:
		raise Http404
	
	filepath = settings.PPT_FILEPATH + folder + '/jpg/'+filename + '.JPG'
	
	try:
		f = open(filepath, 'rb')
		return HttpResponse(f.read())
	except:
		raise Http404



