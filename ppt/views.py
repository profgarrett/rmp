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


#########
# General
#########


def homepage(request):
    user = request.user

    return render_to_response('ppt/index.html',
            {   'user': user,
            },
            context_instance=RequestContext(request))



#########
# Users
#########


@login_required
def user_list(request):
    users = User.objects.all()
        
    return render_to_response('ppt/user_list.html',
            {'users': users}, context_instance=RequestContext(request)
    )


@login_required
def user_view(request, username=False):
    if not username:
        username = request.user

    user = get_object_or_404(User, username=username)
    
    ppts = Ppt.objects.filter(user_id=user.id).order_by('pk')
    
    return render_to_response('ppt/user_view.html',
            {   'user': user,
                'ppts': ppts
            },
            context_instance=RequestContext(request)
    )


##############
# PowerPoints
###############

@login_required
def user_ppt_view(request, username, ppt_id):
    user = get_object_or_404(User, username=username)
    ppt = Ppt.objects.get(user_id=user.id, id=ppt_id)
    
    return render_to_response('ppt/user_ppt_view.html',
            {   'user': user,
                'ppt': ppt,
            },
            context_instance=RequestContext(request)
    )


# Return a jpg image.
@login_required
def user_ppt_jpg(request, username, ppt_id, slide):
    user = get_object_or_404(User, username=username)
    if '..' in folder or '..' in filename:
        raise Http404

    filepath = '%suserfiles/pptfile/%s/%s/jpg/Slide%s.JPG' % (settings.PPT_FILEPATH, user.id, ppt_id, slide)
    try:
        f = open(filepath, 'rb')
        return HttpResponse(f.read())
    except:
        raise Http404


# Note that this both uploads new files and allows edits.
@login_required
def user_ppt_edit(request, username, ppt_id=False):
    user = User.objects.get(username=request.user)

    print(ppt_id)

    if not ppt_id == False:
        ppt = get_object_or_404(Ppt, id=ppt_id)
    else:
        ppt = Ppt(user=user, title='', description='')

    if request.method == 'POST':
        pptForm = PptForm(request.POST, request.FILES, instance=ppt)
        if pptForm.is_valid():
            ppt = pptForm.save()
            return HttpResponseRedirect(ppt.get_absolute_url())
    else:
        pptForm = PptForm(instance=ppt)
    
    return render_to_response('ppt/user_ppt_edit.html',
            {'user': user, 'form': pptForm},
            context_instance=RequestContext(request)
    )


#########
# Units
#########

@login_required
def unit_list(request):
    units = PptUnit.objects.all()
        
    return render_to_response('ppt/unit_list.html',
            {'units': units}, context_instance=RequestContext(request)
    )


@login_required
def unit_view(request, unit_id):
    unit = get_object_or_404(PptUnit, id=unit_id)
        
    return render_to_response('ppt/unit_view.html',
            {'unit': unit}, context_instance=RequestContext(request)
    )



