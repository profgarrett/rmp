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
from exp2_turk.models import *
from exp2_turk.forms import *


@login_required
def ppt_survey_pre(request):
    
    if request.method == 'POST':
        form = PptInitialSurvey1(request.POST)
        if form.is_valid():
            # Save pre form
            new_rating = form.save(commit=False)
            new_rating.user = request.user
            new_rating.save()

            # Find a random falling into 2014 Summer Experiment 2 Turk & goto it.
            unit = PptUnit.objects.filter(title='2014 Summer Experiment 2 Turk')[0]
            ppts = unit.ppt_set.all()
            ppt = ppts[random.randint(0,len(ppts)-1)]

            return HttpResponseRedirect('/exp2_turk/%s/video1' % (ppt.id))
    else:
        form = PptInitialSurvey1()
    
    return render_to_response('exp2_turk/survey_pre.html',
            {'form': form},
            context_instance=RequestContext(request))


@login_required
def ppt_survey_video1(request, experiment, ppt_id):
    ppt = Ppt.objects.get(id=ppt_id)

    transitions = "0, 14, 51, 100, 162, 189, 242, 999"
    youtube = '-0LuDdnjvLc'

    return render_to_response('exp2_turk/survey_video1.html',
            {   'ppt': ppt, 
                'jpgs': ppt.pptjpg_set.all().order_by('filename'),
                'transitions': transitions,
                'youtube': youtube,
                'experiment': experiment
            },
            context_instance=RequestContext(request))



@login_required
def ppt_survey_video2(request, ppt_id):
    ## Fill out a survey on the watched video 
    ppt = Ppt.objects.get(id=ppt_id)

    form1 = PptPostSlideSurvey1

    if request.method == 'POST':
        form1 = form1(request.POST)

        if form1.is_valid() and form2.is_valid():
            new_rating = form1.save(commit=False)
            new_rating.user = request.user
            new_rating.ppt = ppt
            new_rating.save()

            return HttpResponseRedirect('/exp2_turk/thanks.html')
    else:
        form1 = form1()
    
    return render_to_response('exp2_turk/survey_video2.html',
            {   'ppt': ppt, 
                'form1': form1,
                'experiment': experiment
            },
            context_instance=RequestContext(request))


@login_required
def ppt_survey_post(request):
    return render_to_response('exp2_turk/survey_post.html',{},
            context_instance=RequestContext(request))    