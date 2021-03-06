from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from adminsites import cardAdmin
admin.autodiscover()

urlpatterns = patterns('',

                       # index
                       (r'^$', 'card.views.index'),
                       (r'^/?$', 'card.views.index'),
                       (r'^index/?$', 'card.views.index'),
                       (r'^index/err/?$', 'card.auth.login_err'),

                       # login page/functions for CAS (members and checkers)
                       (r'^cas/?$', 'card.auth.cas_login'),

                       # MEMBER
                       # personal
                       (r'^(?P<netid>\w+)/personal/?$', 'card.views.personal'),
                       # CHECKER
                       # Meal checking
                       (r'^(?P<netid>\w+)/checker/session/?$', 'card.checksession.open_session'),
                       (r'^(?P<netid>\w+)/checker/check/?$', 'card.checksession.open_session_check'),
#                       (r'(?P<netid>\w+)/checker/register/?$', 'card.checksession.open_session_reg'),
                       # Session
                       (r'^(?P<netid>\w+)/session/add/?$', 'card.checksession.check_session'),
#                       (r'(?P<netid>\w+)/session/add/remove/(?P<meal_idx>\w+)/?$', 'card.checksession.remove_meal'),                       
#                       (r'(?P<netid>\w+)/session/register/?$', 'card.register.reg_session'),
#                       (r'(?P<netid>\w+)/session/register/remove/(?P<mem_idx>\w+)/?$', 'card.register.remove_mem'),

                       # CLUB ACCOUNT
                       # club login
                       (r'^club/?$', 'card.auth.club_login'),
                       # default
                       (r'^(?P<club>\w+)/club/?$', 'card.club.club'),
                       # Members functions
                       (r'^(?P<club>\w+)/members/add/?$', 'card.register.registerClub'),
                       (r'^(?P<club>\w+)/members/list/?$', 'card.club.listMembers'),
                       (r'^(?P<club>\w+)/members/(?P<netid>\w+)/modify/?$', 'card.club.modMember'),
                       # Meals functions
                       (r'^(?P<club>\w+)/meals/add/?$', 'card.club.addMeals'),
                       (r'^(?P<club>\w+)/meals/(?P<mealid>\w+)/modify/?$', 'card.club.modMeals'),
                       (r'^(?P<club>\w+)/meals/list/?$', 'card.club.listMeals'),
                       # Statistics
                       (r'^(?P<club>\w+)/stats/(?P<graphtype>\w+)/?$', 'card.club.stats'),
                       # Change password
                       (r'^(?P<club>\w+)/account/?$', 'card.auth.change_password'),
                       # General logout
                       (r'^logout_cas/?$', 'card.auth.cas_logout'),
                       (r'^logout_club/?$', 'card.auth.club_logout'),

                       # help documentation
                       (r'^help/(?P<path>.*)$', 'card.views.help'),

                       
                       # Admin - not upgradable since it doesn't use django_cas
                       (r'^admin/', include(admin.site.urls)),
                       #url(r'^admin/?$', 'django_cas.views.login', kwargs={'next_page': '/djadmin/'}),
                       #(r'^djadmin/', include(admin.site.urls)),

                       (r'^cardAdmin/', include(cardAdmin.urls)),
                       #(r'^admin/*(.*)',admin.site.root),
)

urlpatterns += staticfiles_urlpatterns()

