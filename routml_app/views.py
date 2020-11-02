from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import Url
from .utils import encode, decode, reverse_querystring, is_valid_url, is_valid_url_id

def index(request):
    if request.method == "GET":
        url_id = request.GET.get("u", None)

        if url_id is None:
            return render(request, "routml_app/index.html")
        
        if not is_valid_url_id(url_id):
            return render(request, "routml_app/error.html", {
                "err_code": "404",
                "err_msg": "URL not found",
            }, status=404)
        
        url_id = decode(url_id)
        url = Url.objects.filter(id=url_id).first()

        if url is None:
            return render(request, "routml_app/error.html", {
                "err_code": "404",
                "err_msg": "URL not found",
            }, status=404)
        
        return render(request, "routml_app/display.html", {
                "url": "http://rout.ml/" + encode(url.id)
            })
    
    if request.method == "POST":
        url = request.POST.get("u", None)

        if url is None or url == "":
            return render(request, "routml_app/error.html", {
                "err_code": "400",
                "err_msg": "No URL provided",
            }, status=400)
        
        if not is_valid_url(url):
            return render(request, "routml_app/error.html", {
                "err_code": "400",
                "err_msg": "Invalid URL",
            }, status=400)
        
        old_url = Url.objects.filter(url=url).first()
    
        if old_url is not None:
            date = datetime.datetime.now()
            old_url.day = date.day
            old_url.month = date.month
            old_url.year = date.year
            old_url.save()
            old_url_id = encode(old_url.id)
            return HttpResponseRedirect(reverse_querystring("index", query_kwargs={"u": old_url_id}))
        
        date = datetime.datetime.now()
        new_url = Url(url=url, day=date.day, month=date.month, year=date.year)
        new_url.save()
        new_url_id = encode(new_url.id)

        return HttpResponseRedirect(reverse_querystring("index", query_kwargs={"u": new_url_id}))

    return render(request, "routml_app/error.html", {
        "err_code": "400",
        "err_msg": "Method not allowed",
    }, status=400)

def redirect_to_url(request, url_id=None):
    if url_id is None:
        return HttpResponseRedirect(reverse("index"))
    
    if not is_valid_url_id(url_id):
        return render(request, "routml_app/error.html", {
            "err_code": "404",
            "err_msg": "URL not found",
        }, status=404)

    url_id = decode(url_id)
    url = Url.objects.filter(id=url_id).first()
    
    if url is None:
        return render(request, "routml_app/error.html", {
            "err_code": "404",
            "err_msg": "URL not found",
        }, status=404)
    
    return HttpResponseRedirect(url.url)
