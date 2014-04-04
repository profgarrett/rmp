from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings

import os
import random

from ppt.models import *
from ppt.forms import *
from exp1.models import *
from exp1.forms import *

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
            ppt = unit.ppt_set.all()[random.randint(0,1)]

            return HttpResponseRedirect('/exp1/A/%s/video1' % (ppt.id))
    else:
        form = PptInitialSurvey1()
    
    return render_to_response('exp1/survey_pre.html',
            {'form': form},
            context_instance=RequestContext(request))


@login_required
def ppt_survey_video1(request, experiment, ppt_id):
    ppt = Ppt.objects.get(id=ppt_id)

    if experiment == 'A':
        transitions = "0, 14, 51, 100, 162, 189, 242, 999"
        youtube = '-0LuDdnjvLc'
    elif experiment == 'B':
        transitions = "0, 19, 43, 105, 140, 186, 211, 999"
        youtube = '8NyIv47tIEM'
    elif experiment == 'C':
        transitions = "0, 15, 62, 110, 131, 155, 220, 999"
        youtube = 'tG8VzFBy6Ew'
    elif experiment == 'D':
        transitions = "0, 18, 61, 101, 170, 206, 234, 999"
        youtube = 'fPiLAX3piB8'
    elif experiment == 'E':
        transitions = "0, 11, 37, 85, 148, 194, 210, 999"
        youtube = 'sNa0uiZVrA8'

    return render_to_response('exp1/survey_video1.html',
            {   'ppt': ppt, 
                'jpgs': ppt.pptjpg_set.all().order_by('filename'),
                'transitions': transitions,
                'youtube': youtube,
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

            # Find a random falling into next experiment & goto it (unless we're done!)
            if nextexperiment=='Z':
                return HttpResponseRedirect('/exp1/thanks.html')
            else:
                unit = PptUnit.objects.filter(title='2014 Summer Experiment '+nextexperiment)[0]
                ppt = unit.ppt_set.all()[random.randint(0,1)]
                return HttpResponseRedirect('/exp1/%s/%s/video1' % (nextexperiment, ppt.id))
    else:
        form1 = form1()
        form2 = form2()
    
    return render_to_response('exp1/survey_video2.html',
            {   'ppt': ppt, 
                'form1': form1,
                'form2': form2, 
                'experiment': experiment
            },
            context_instance=RequestContext(request))


@login_required
def ppt_survey_post(request):

    return render_to_response('exp1/survey_post.html',{},
            context_instance=RequestContext(request))    