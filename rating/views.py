from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
#from django.contrib import auth
#from django.contrib.auth import forms, models
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings

import os
import random

from rating.models import *
from rating.forms import *
from rating.parser import HtmlParser
from rating.utility import ScaledPage


@login_required
def homepage(request):
    user = request.user

    ratings = PptRating.objects.filter(user__username=user).order_by('-ratedate')

    return render_to_response('rating/index.html',
            {   'username': user.username,
                'count': ratings.count(),
                'ratings': ratings.all()
            },
            context_instance=RequestContext(request))


@login_required
def goto_random(request):
    
    ppt_list = Ppt.objects.filter(user__username='pearson')
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
            {   'user': user,
                'ppts': ppts
            },
            context_instance=RequestContext(request)
    )


@login_required
def user_ppt_view(request, username, ppt_id):
    user = get_object_or_404(User, username=username)
    ppt = Ppt.objects.get(user_id=user.id, id=ppt_id)
    
    ratings = PptRating.objects.filter(ppt_id=ppt_id)
    jpgs = ppt.jpgs()
    
    return render_to_response('rating/user_ppt_view.html',
            {   'user': user,
                'ppt': ppt,
                'jpgs': jpgs,
                'ratings': ratings
            },
            context_instance=RequestContext(request)
    )


@login_required
def tag_view(request, tag):
    ppttags = PptTag.objects.filter(tag=tag)
    pptunittags = PptUnitTag.objects.filter(tag=tag)
        
    return render_to_response('rating/tag_view.html',
            {   'tag': tag,
                'ppttags': ppttags,
                'pptunittags': pptunittags
            }, context_instance=RequestContext(request)
    )


@login_required
def user_list(request):
    users = User.objects.all()
        
    return render_to_response('rating/user_list.html',
            {'users': users}, context_instance=RequestContext(request)
    )


@login_required
def unit_view(request, unit_id):
    unit = get_object_or_404(PptUnit, id=unit_id)
        
    return render_to_response('rating/unit_view.html',
            {'unit': unit}, context_instance=RequestContext(request)
    )


@login_required
def user_ppt_view_metadata(request, username, ppt_id):
    
    user = get_object_or_404(User, username=username)
    ppt = Ppt.objects.get(user_id=user.id, id=ppt_id)
    #ratings = PptRating.objects.filter(ppt_id=ppt_id)
    HtmlParser(ppt, True)
    pptHtmlPages = PptHtmlPage.objects.filter(ppt_id=ppt_id).order_by('order').all()

    return render_to_response('rating/user_ppt_view_metadata.html',
            {   'user': user,
                'ppt': ppt,
                'scaledPages': [ScaledPage(p, 500) for p in pptHtmlPages],
            },
            context_instance=RequestContext(request)
    )


# Return a html file index.
@login_required
def user_ppt_htm(request, username, ppt_id):
    user = get_object_or_404(User, username=username)
    
    filepath = '%suserfiles/pptfile/%s/%s/html.htm' % (settings.PPT_FILEPATH, user.id, ppt_id)
    try:
        f = open(filepath, 'rb')
        return HttpResponse(f.read())
    except:
        raise Http404


# Return a jpg image.
@login_required
def user_ppt_jpg(request, username, ppt_id, slide):
    user = get_object_or_404(User, username=username)
    
    filepath = '%suserfiles/pptfile/%s/%s/jpg/Slide%s.JPG' % (settings.PPT_FILEPATH, user.id, ppt_id, slide)
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
    
    filepath = '%suserfiles/pptfile/%s/%s/html_files/%s' % (settings.PPT_FILEPATH, user.id, ppt_id, filename)
    print filepath
    try:
        f = open(filepath, 'rb')
        return HttpResponse(f.read())
    except:
        raise Http404


@login_required
def user_ppt_upload(request, username):
    
    if request.method == 'POST':
        
        pptForm = PptForm(request.POST, request.FILES)
        
        if pptForm.is_valid():
            
            # Save Ppt record
            ppt = pptForm.save(commit=False)
            ppt.user = request.user
            ppt.folder = ''
            ppt.filename = ''
            ppt.rnd = random.randint(0, 1000000000)
            ppt.unit_id = 0
            ppt.save()
            pptForm.save_m2m()
            
            return HttpResponseRedirect(ppt.get_absolute_url())
        
    else:
        pptForm = PptForm()
    
    return render_to_response('rating/upload.html',
            {'pptForm': pptForm},
            context_instance=RequestContext(request)
    )


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
        jpgs = ppt.jpgs()
        print jpgs
        if False and not os.path.exists(jpg):
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
        
        form = PptRatingForm()
    
    return render_to_response('rating/rate.html',
            {'ppt': ppt, 'jpgs': jpgs, 'form': form},
            context_instance=RequestContext(request))


# Return a jpg image.
@login_required
def ppt_jpg(request, folder, filename):
    if '..' in folder or '..' in filename:
        raise Http404
    
    filepath = settings.PPT_FILEPATH + folder + '/jpg/' + filename + '.JPG'
    
    try:
        f = open(filepath, 'rb')
        return HttpResponse(f.read())
    except:
        raise Http404


## Experiment 2014

@login_required
def ppt_survey_pre(request):
    
    if request.method == 'POST':
        form = PptInitialSurvey1(request.POST)
        if form.is_valid():
            # Save pre form
            new_rating = form.save(commit=False)
            new_rating.user = request.user
            new_rating.save()

            # Find a random falling into 2014 Summer Experiment A & goto it.
            unit = PptUnit.objects.filter(title='2014 Summer Experiment A')[0]
            ppt = unit.ppts.all()[random.randint(0,1)]

            return HttpResponseRedirect('/experiment/A/%s/video1' % (ppt.id))
    else:
        form = PptInitialSurvey1()
    
    return render_to_response('rating/survey_pre.html',
            {'form': form},
            context_instance=RequestContext(request))


@login_required
def ppt_survey_video1(request, experiment, ppt_id):
    ppt = Ppt.objects.get(id=ppt_id)
    jpgs = ppt.jpgs()

    if experiment == 'A':
        transitions = "0, 14, 51, 100, 162, 189, 242, 999"
    elif experiment == 'B':
        transitions = "0, 19, 43, 105, 140, 186, 224, 999"
    elif experiment == 'C':
        transitions = "0, 15, 62, 110, 131, 155, 220, 999"
    elif experiment == 'D':
        transitions = "0, 18, 61, 101, 170, 206, 234, 999"
    elif experiment == 'E':
        transitions = "0, 11, 37, 85, 148, 194, 210, 999"

    return render_to_response('rating/survey_video1.html',
            {   'ppt': ppt, 
                'transitions': transitions,
                'jpgs': jpgs, 
                'experiment': experiment
            },
            context_instance=RequestContext(request))



@login_required
def ppt_survey_video2(request, experiment, ppt_id):
    ## Fill out a survey on the watched video 
    ppt = Ppt.objects.get(id=ppt_id)

    form1 = PptPostSlideSurvey1

    if experiment == 'A':
        form2 = PptTopicA
        nextexperiment = "B"
    elif experiment == 'B':
        form2 = PptTopicB
        nextexperiment = "C"
    elif experiment == 'C':
        form2 = PptTopicC
        nextexperiment = "D"
    elif experiment == 'D':
        form2 = PptTopicD
        nextexperiment = "E"
    elif experiment == 'E':
        form2 = PptTopicE
        nextexperiment = "Z"

    if request.method == 'POST':
        form1 = form1(request.POST)
        form2 = form2(request.POST)

        if form1.is_valid() and form2.is_valid():
            new_rating = form1.save(commit=False)
            new_rating.user = request.user
            new_rating.ppt = ppt
            new_rating.save()

            new_rating = form2.save(commit=False)
            new_rating.user = request.user
            new_rating.ppt = ppt
            new_rating.save()

            # Find a random falling into next experiment & goto it (unles we're done!)
            if nextexperiment=='Z':
                return HttpResponseRedirect('/experiment/thanks.html')
            else:
                unit = PptUnit.objects.filter(title='2014 Summer Experiment '+nextexperiment)[0]
                ppt = unit.ppts.all()[random.randint(0,1)]
                return HttpResponseRedirect('/experiment/%s/%s/video1' % (nextexperiment, ppt.id))
    else:
        form1 = form1()
        form2 = form2()
    
    return render_to_response('rating/survey_video2.html',
            {   'ppt': ppt, 
                'form1': form1,
                'form2': form2, 
                'experiment': experiment
            },
            context_instance=RequestContext(request))


@login_required
def ppt_survey_post(request):

    return render_to_response('rating/survey_post.html',{},
            context_instance=RequestContext(request))    