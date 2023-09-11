from django.shortcuts import render,redirect

# Create your views here.

import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import time
from django.contrib.auth.models import User


def dashboard(request):
    try:    
        if request.session['_auth_user_id'] :
                uu=User.objects.filter(id=request.session['_auth_user_id']).first()
    except:
        return redirect('/accounts/login/')                
    return redirect('/')

# Dictionary to store timestamps for keywords
keyword_timestamps = {}

def can_make_search(keyword, threshold_seconds=900):  # 900 seconds = 15 minutes
    current_time = time.time()
    
    if keyword in keyword_timestamps:
        last_search_time = keyword_timestamps[keyword]
        
        if current_time - last_search_time < threshold_seconds:
            # Search request is within the threshold, disallow it
            return False
    
    # Update or add the timestamp for the keyword
    keyword_timestamps[keyword] = current_time
    print('keyword_timestamps',keyword_timestamps)
    return True

def get_news(request):
    api_key = 'a2173a3b372e49ea9f39007b63578e69'
    sekeyword=''
    params=''
    api_url = 'https://newsapi.org/v2/top-headlines'
 
    if request.method == "POST" and 'bnt_submit' in request.POST:
        keyword = request.POST['keyword']
        
        if can_make_search(keyword):  
            
            if not SearchResult.objects.filter(keyword=keyword):
                SearchResult.objects.create(keyword=keyword,user_id=request.session['_auth_user_id'])
            
            # making the API request
            sekeyword = keyword
            params = {
                'q': keyword,
                # 'country': 'us',
                # 'language': 'english',
                'sortBy': 'Date published',
                'apiKey': api_key,
            }
        else:
            params = {
            'q':'china',
            # 'country': 'us',  
            #'language':'english',
            'apiKey': api_key,
            }   
            print('wait for some time')
            # Make the API request and process the results

    elif  request.method=="POST" and 'bnt_refresh' in request.POST:
        keyword=request.POST['keyword']
        sekeyword=keyword
        params = {
            'q':keyword,
            # 'country': 'us',  
            #'language':'english',
            'sortBy':'Date published',
            'apiKey': api_key,
        }
        if not SearchResult.objects.filter(keyword=keyword):
            SearchResult.objects.create(keyword=keyword,user_id=request.session['_auth_user_id'])
    elif  request.method=="POST" and 'bnt_filter' in request.POST:
        keyword=request.POST['keyword']
        Date_published=request.POST['Date_published']
        Name=request.POST['Name']
        Category=request.POST['Category']
        language=request.POST['language']
        sekeyword=keyword
        params = {
            'q':keyword,
            # 'country': 'us',  
            'from':Date_published,
            'source':{'name':Name},
            'language':'language',
            'sortBy':'Date published',
            'apiKey': api_key,
        }
        if not SearchResult.objects.filter(keyword=keyword):
            SearchResult.objects.create(
                keyword=keyword,
            )
                        
    else:
        params = {
            'q':'india',
            # 'country': 'us',  
            #'language':'english',
            'apiKey': api_key,
        }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        articles = data['articles']
        return render(request, 'news.html', {'articles': articles,'sekeyword':sekeyword})
    
    else:
        return HttpResponse(f'Error: {response.status_code} - {response.text}')

def search_history(request):
    if request.session['_auth_user_id'] :
        # list=SearchResult.objects.all().delete()
        list=SearchResult.objects.filter(id=request.session['_auth_user_id'])
    return render(request,'search_history.html',{'list':list})