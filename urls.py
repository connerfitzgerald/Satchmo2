from django.conf.urls.defaults import *

from satchmo_store.urls import urlpatterns

urlpatterns += patterns('',
    (r'^library/', 'store.library.views.lib'),
    (r'^books/(?P<book>[a-zA-Z0-9_.-]+)/$', 'store.library.views.book'),
    (r'^books/(?P<book>[a-zA-Z0-9_.-]+)/(?P<second>[a-zA-Z0-9_.-]+)/$', 'store.library.views.second'),
    (r'^books/(?P<book>[a-zA-Z0-9_.-]+)/(?P<second>[a-zA-Z0-9_.-]+)/(?P<third>[a-zA-Z0-9_.-]+)/$', 'store.library.views.third'),
    (r'^books/(?P<book>[a-zA-Z0-9_.-]+)/(?P<second>[a-zA-Z0-9_.-]+)/(?P<third>[a-zA-Z0-9_.-]+)/(?P<fourth>[a-zA-Z0-9_.-]+)/$', 'store.library.views.fourth'),
    (r'^booksDUMMY/(?P<path>.*)$', 'store.library.views.alternative',{'document_root': '/Users/ben/RandomCode/DjangoProjects/RentalModel_0.1a/store/mediasecure'}),
)
