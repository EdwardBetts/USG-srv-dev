################################################################
# Project: Princeton Events Calendar
# Authors: Ethan Goldstein, Samantha Hantman, Dana Hoffman, 
#           Adriana Susnea, and Michael Yaroshefsky 
# Date:    May 11, 2010
################################################################
# Title:  views_users.py
# Info :  rendering user pages (profile, personal events, etc.)
################################################################

from django.http import *
from render import render_to_response
from django.contrib.auth import login
import urllib, re
from datetime import datetime, timedelta
from models import *
from cauth import *
from rsvp import *
from forms import *
from views_events import *
from cal import query
from decorators import login_required


@login_required
def user_profile(request):
   try:
      if request.method =='POST':
         profileForm = EditUserForm(request.POST, instance=request.session['user_data'])
         if profileForm.is_valid():
            user = profileForm.save()
            request.session['user_data']=user
            Msg("Profile successfully updated", 1).push(request)
         if 'newbie' in request.GET:
            if 'login_redirect' in request.session:
               referrer = request.session['login_redirect']
               del request.session['login_redirect']
               return HttpResponseRedirect(referrer)
            else:
               return HttpResponseRedirect('/')
         
      else:
         profileForm = EditUserForm(instance=request.session['user_data'])
   
      dict = {'profileForm':profileForm}

   except KeyError:
      dict = {}
   
   return render_to_response(request, 'cal/user_profile.html', dict )


@login_required
def user_events(request):
    upcoming = user_upcoming_events(request)
    created = user_created_events(request)
    dict = {
        'evlist_inner': upcoming + "<div style='padding:32px 0;'><hr style='border-top:1px solid #888;'/></div>" + created,
        'feat_opts': EventFeature.objects.all(),
    }
    return evlist_render_page(request, dict)


@login_required
def user_upcoming_events(request):
    user = current_user(request)
    dict ={}
    rsvps = RSVP.objects.exclude(rsvp_event__event_date_time_start=dtdeleteflag).filter(rsvp_user=current_user(request),rsvp_type='Accepted',rsvp_event__event_date_time_start__gte=datetime.now()).order_by('rsvp_event__event_date_time_start')
    grouped_events = query.rsvps2grouped(rsvps, Event.getFormattedStartDate)
    dict['evinner_title'] = "My Upcoming Events"
    dict['grouped_events'] = grouped_events
    return render_to_string("cal/evlist_inner.html", dict)


@login_required
def user_past_events(request):
    """
    no active link to this page
    """
    user = current_user(request)
    dict = {}
    rsvps = RSVP.objects.exclude(rsvp_event__event_date_time_start=dtdeleteflag).filter(rsvp_user=current_user(request),rsvp_type='Accepted',rsvp_event__event_date_time_start__lte=datetime.now()).order_by('rsvp_event__event_date_time_start')
    grouped_events = query.rsvps2grouped(rsvps, Event.getFormattedStartDate)
    dict['evinner_title'] = "My Past Events"
    dict['grouped_events'] = grouped_events
    return render_to_string("cal/evlist_inner.html", dict)


@login_required
def user_created_events(request):
    user = current_user(request)
    dict = {}
    events = Event.objects.exclude(event_date_time_start=dtdeleteflag).filter(event_cluster__cluster_user_created=current_user(request)).order_by('event_date_time_start')
    grouped_events = query.events2grouped(events, Event.getFormattedStartDate, None)
    dict['evinner_title'] = "Events I've Created"
    dict['grouped_events'] = grouped_events
    return render_to_string("cal/evlist_inner.html", dict)


@login_required
def user_invitations(request):
    """
    should move into my my events
    """
    dict = {}
    user = current_user(request)
    dict['pending_invites'] = RSVP.objects.filter(rsvp_user=user,rsvp_event__event_date_time_start__gte=datetime.now(),rsvp_type='Pending').order_by('rsvp_event__event_date_time_start')
    dict['accepted_invites'] = RSVP.objects.filter(rsvp_user=user,rsvp_type='Accepted',rsvp_referrer__isnull=False, rsvp_event__event_date_time_start__gte=datetime.now()).order_by('rsvp_event__event_date_time_start')
    dict['declined_invites'] = RSVP.objects.filter(rsvp_user=user,rsvp_type='Declined', rsvp_event__event_date_time_start__gte=datetime.now() ).order_by('rsvp_event__event_date_time_start')
    return render_to_response(request, 'cal/user_invites.html', dict)     


@login_required
def user_messages(request):
    """
    no active link to this... we should replace my invites with my messages and move invites to my events
    """
    dict = {}
    user = current_user(request)
    all_messages = UserMessage.objects.filter(um_user = user).order_by('um_date_posted').reverse()
    dict['unread_messages'] = UserMessage.objects.filter(um_user = user, um_date_read = None).order_by('um_date_posted').reverse()
    len(dict['unread_messages']) #Evaluate it now!
    dict['read_messages'] = UserMessage.objects.filter(um_user = user).exclude(um_date_read = None).order_by('um_date_posted').reverse()[0:5]
    len(dict['read_messages']) #Evaluate it now!
    for msg in dict['unread_messages']:
         msg.mark_read()
    return render_to_response(request, 'cal/user_messages.html', dict)


