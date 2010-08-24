import string
from library.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import *
import os
import posixpath
import mimetypes
from product.models import Product

def lib(request):
# Create your views here.
    u1= User.objects.get(username= request.user)
    UP= UserProfile.objects.get(user=u1)
    VP = UP.viewingpermission_set.all()
#            print u1.id
#            print item.product.id
#    Book = Product.objects.get(id=item.product.id)
    return render_to_response('base123.html', {'VP': VP} )
    
    
def book(request,book='0'):
#    return render_to_response('../../static/books/DRMTest/flipviewerxpress.html')
#    return render_to_response('books/DRMTest/flipviewerxpress.html')
    return render_to_response('books/'+ str(book) + '/flipviewerxpress.html',{'book':book})
    
    try:
   # Division by zero raises an exception
        b = Product.objects.get(slug=book)
        u1= User.objects.get(username= request.user)
        UP= UserProfile.objects.get(user=u1)
        VP= UP.viewingpermission_set.all()
        for x in VP:
         if (str(x.BookKey) == str(b.name)):
          print (str(b.slug)+'.html')
          return render_to_response('book.html', {'book': book})
#          return render_to_response('../static/books/DRMTest/flipviewerxpress.html') 
          #str(b.name)+'.html')
    except :
        print "Oops, invalid."
        return render_to_response('failure.html', {'book': book})
    else:
        print "else loop"
        return render_to_response('failure.html', {'book': book})



    
def second(request,book='0',second='0'):
#    return render_to_response('../../static/books/DRMTest/flipviewerxpress.html')
#    return render_to_response('books/DRMTest/flipviewerxpress.html')
    return render_to_response('books/'+ str(book) + '/' + str(second), {'book':book }) 
    
def third(request,book='0',second='0',third='0'):
#    return render_to_response('../../static/books/DRMTest/flipviewerxpress.html')
#    return render_to_response('books/DRMTest/flipviewerxpress.html')
    return render_to_response('books/'+ str(book) + '/' + str(second)+ '/' + str(third), {'book':book, 'second':second,'third':third})     
    
def fourth(request,book='0',second='0',third='0'):
#    return render_to_response('../../static/books/DRMTest/flipviewerxpress.html')
#    return render_to_response('books/DRMTest/flipviewerxpress.html')
    return render_to_response('books/'+ str(book) + '/' + str(second)+ '/' + str(third)+'/' + str(fourth), {'book':book, 'second':second,'third':third,'fourth':fourth})     
    
    
def alternative(request,path='0',document_root=None):
    PathParts = path.split('/')
    '''jesus wept keep an eye on this shamefully its slightly hardcoded'''
    book= PathParts[1]
    print book
    b = Product.objects.get(slug=str(book))
    print b.name
    try:
   # Division by zero raises an exception
        b = Product.objects.get(slug=book)
        print b.name
        u1= User.objects.get(username= request.user)
        print u1
        UP= UserProfile.objects.get(user=u1)
        VP= UP.viewingpermission_set.all()
        for x in VP:
         if (str(x.BookKey) == str(b.name)):
          print (str(b.slug)+'.html')
          fullpath = os.path.join(document_root, path)
          print (fullpath)
          mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
          contents = open(fullpath, 'rb').read()
          response = HttpResponse(contents, mimetype=mimetype)
          return response
    
    except :
        print "Oops, invalid."
        return render_to_response('failure.html', {'book': book})
        
    
    
    
    
    
    
    
    