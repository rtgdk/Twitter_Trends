from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django import forms
from django.template import RequestContext
from pymongo import MongoClient
import tweepy
from twython import Twython
from pymongo import MongoClient
import math
import datetime
import json
import random
from tqdm import tqdm
from .models import Woeid
# Create your views here.

#dbclient = MongoClient('mongodb://admin:admin@54.80.161.204:27017')
#dbclient = MongoClient('mongodb://admin:admin@54.172.143.59:27017')
dbclient = MongoClient('mongodb://admin:admin@54.172.130.187:27017')

db_trends = dbclient['Twitter_Trends']
#db_coll = db_trends.Trends_Place
    
def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
    return abs((d2 - d1).days)


def index(request):
    context_dict = {}
    count = 0
    print "here"
    db_coll_rate = db_trends.Trends_Rate
    d=list(db_coll_rate.find({}).sort("Rate_Increase", -1))
    print "rate done"
    (newt2,topr2) = fetch_all("India",d)
    print "India done"
    # print "newt2"
    # print newt2
    print "\nnewt2\n"
    print newt2
    print "\ntopr2\n"
    print topr2
    (newt1, topr1) = fetch_all("Worldwide",d)
    print "Worldwide done"
    context_dict["newt2"] = newt2 #top_trends_fetch("India")   #newt2
    context_dict["newt1"] = newt1#top_trends_fetch("Worldwide") #newt1
    context_dict["country2"] = "India"
    context_dict["country1"] = "Worldwide"
    context_dict["country3"] = "Worldwide"
    context_dict["country4"] = "India"
    context_dict['topr'] = topr1
    context_dict['topr2'] =topr2
    #context_dict["tweets"] = hlist
    # context_dict["volume"]= tvlist
    # context_dict["rate"]= rlist
    # context_dict["count"] = count
    return render(request, 'app/index.html', context_dict)


#from operator import itemgetter

# woeid = "India"

def fetch_all(woeid,d):
    a=[]
    b=[]
    db_coll_trends = db_trends.Trends_Place
    db_coll_rate = db_trends.Trends_Rate
    #tdate = str(datetime.date.today())+"T00:00:00Z"
    tdate ='2017-06-18T00:00:00Z'
    dict_trends = list(db_coll_trends.find({"Name": woeid,"Timestamp": {"$gt": tdate}}).sort('_id', -1))
    ul=[]
    count = 0
    for trend in tqdm(dict_trends):
        if count>100:
            break
        if (ul.count(trend['Hashtag'])==0):
            count= count+1
            dict_top3={}
            try:
                ul.append(trend['Hashtag'])
                dict_top3.update({"name": trend['Hashtag'].replace(" ", "__")})
                count = count + 1
                score = len(db_coll_trends.find({"Hashtag":trend['Hashtag']}).distinct("Woeid"))
                dict_top3.update({"score": score})
                ri = round(list(db_coll_rate.find({"Hashtag":trend['Hashtag']}))[0]["Rate_Increase"],2)
                dict_top3.update({"ri": ri})
            except:
                dict_top3.update({"name": trend['Hashtag'].replace(" ", "__")})
                dict_top3.update({"score": 1})
                dict_top3.update({"ri": 1})
            a.append(dict_top3)
    sorted_dict3 = sorted(a, key=lambda k: k['score'], reverse=True)
    print sorted_dict3
    print ("Trends done")
    distinct_dict_trends = ({v['Hashtag']: v for v in dict_trends})
    print("Distinct")
    print distinct_dict_trends
    count = 0;
    for i in tqdm(distinct_dict_trends):
        if count > 50:
            break
        try:
            dict_tr = {}
            ri = list(filter(lambda person: person['Hashtag'] == i["Hashtag"], d))[0]["Rate_Increase"]
            dict_tr.update({"name":i.replace(" ", "__")})
            dict_tr.update({"ri":round(ri,2)})
            find_hash = list(filter(lambda person: person['Hashtag'] == i["Hashtag"], dict_trends))
            score = ({v['Woeid']: v for v in find_hash})
            dict_tr.update({"score": len(score)})
        except:
            dict_tr.update({"name":i.replace(" ", "__")})
            dict_tr.update({"ri":1})
            dict_tr.update({"score": 1})
        b.append(dict_tr)
    sorted_dict4 = sorted(b, key=lambda k: k['ri'], reverse=True)
    print ("Rise done")
    return (sorted_dict3,sorted_dict4)

def fetch_top_risers2(woeid):
    db_coll = db_trends.Trends_Place
    db_coll_tr = db_trends.Trends_Rate
    list_tr = db_coll.find({"Name":woeid}).distinct("Hashtag")
    a=[]
    #return a
    print len(list_tr)
    d=list(db_coll_tr.find({}).sort("Rate_Increase", -1))   # trends rate list
    #e=list(db_coll.find({}).sort("_id", -1))           # all trends list
    count = 0
    for i in list_tr:
        #print (i)
        if count >50 :
            break
        try:    
            dict_top={}
            ri = list(filter(lambda person: person['Hashtag'] == i, d))[0]
            dict_top.update({"name":i.replace(" ", "__")})
            dict_top.update({"ri":round(ri["Rate_Increase"],2)})
            score = db_coll.find({"Hashtag":i}, {"Woeid":1}).distinct("Woeid")
            dict_top.update({"score": len(score)})
            a.append(dict_top)
            count = count +1
            print "right"
        except:
            print "wrong"
            pass
    sorted_dict3 = sorted(a, key=lambda k: k['ri'], reverse=True)
    return sorted_dict3
    
                    
def top_trends_fetch(woeid):
    a=[]
    #return a
    db_coll_trends = db_trends.Trends_Place
    dict_trends = db_coll_trends.find({"Name": woeid}).sort([('_id', -1)])
    print dict_trends
    dict_top1 = {}
    dict_top2 = {}
    #current_date = datetime.date.today()
    ul = []
    count = 0
    db_coll_rate = db_trends.Trends_Rate
    for trend in dict_trends:
        if count > 50:
            break
        if (ul.count(trend['Hashtag'])==0):
            ul.append(trend['Hashtag'])
            count = count + 1
            # timestamp = trend['Timestamp']
            # date1 = timestamp[0:10]
            # diff_days = days_between(str(date1), str(current_date))
            # if(diff_days>1):
            #    continue
            dict_top3 = {}
            dict_top3.update({"name": trend['Hashtag'].replace(" ", "__")})
            try:
                    #print db_coll.find({"Hashtag":trend['Hashtag']})
                #tag = list(db_coll.find({"Hashtag":trend['Hashtag']}))[0]
                #print len(tag)
                #vol_dict = tag["Vol_Dict"]
                score = len(db_coll_trends.find({"Hashtag":trend['Hashtag']}).distinct("Woeid"))
                print "score done"
                ri = list(db_coll_rate.find({"Hashtag":trend['Hashtag']}))[0]
                print "rate done"
                #print type(ri)
                #print (ri)
                dict_top3.update({"ri": round(ri["Rate_Increase"],2)})
                print "ri don e"
                #score=0
                #for i in vol_dict:
                    #score = score + len(vol_dict[i])-1
            except:
                #print "wrong"
                score = 1
                dict_top3.update({"ri": 1})
            #dict_top3.update({"score": random.randrange(20,45)})
            dict_top3.update({"score": score})
            a.append(dict_top3)
        else:
            continue
    # dict_top3.update({trend['Hashtag']:score3})
    sorted_dict3 = sorted(a, key=lambda k: k['score'], reverse=True)
    return sorted_dict3



def tweet_fetch(request,woeid, hashtag, count):
    #if (woeid==)
    # return HttpResponse(hashtag)
    hashtag = hashtag.replace("__"," ")
    #dbclient = MongoClient("mongodb://admin:admin@54.172.143.59:27017")
    #db_trends = dbclient['Twitter_Trends']
    db_coll_trends = db_trends.Trends_Place
    hash_dict = db_coll_trends.find({"Hashtag": hashtag})
    if hash_dict.count() == 0:
        hashtag = "#" + hashtag
    #print hashtag +"------------------------------"
    consumer_key6 = '495MzSHQ36Ds9NttT8glVvK79'
    consumer_secret6 = 'cRjX3CITBOtsEqKn2jgj3DBLK8MBgANfdFvNex57PeMlHUMZCY'
    access_token6 = '870132122421403652-Ahmy6auwb8Qzrh8PvXP5E6ZLvEJZQcQ'
    access_token_secret6 = 'fMbbcTik6QamDmqxV3zxwQwCz0CHvclFtYiGZdCEFuqo4'
    auth1 = tweepy.OAuthHandler(consumer_key6, consumer_secret6)
    auth1.set_access_token(access_token6, access_token_secret6)
    api1 = tweepy.API(auth1)
    auth2 = Twython(consumer_key6, consumer_secret6, access_token6, access_token_secret6)
    search1 = api1.search(q=hashtag, result_type='mixed', count=count, include_entities='true')
    search2 = auth2.search(q=hashtag, result_type='mixed', count=count, include_entities='true')
    a = []
    c= []
    d= []
    #print woeid, hashtag
    dict_time = db_coll_trends.find({"Name": woeid, "Hashtag": hashtag})
    #print dict_time
    for i in dict_time:
        timestamp = i['Timestamp']
        c.append(timestamp[11:16])
        d.append(i['Tweet_Volume'])
    print ("Hey ")
    #print c
    #print d
    for i in search2['statuses']:
        #print i['text']
        a.append(i["text"])
    # print ''
    response = {}
    response["tweets"] = a
    response["timestamp"] = c[:20]
    response["tweetvol"] = d[:20]
    b = json.dumps(response)
    #print b
    return HttpResponse(b)
    #print b
    #return HttpResponse(b,e,f)

def fetch_top_risers():
    a=[]
    #return a
    #dbclient = MongoClient('mongodb://admin:admin@54.172.143.59:27017')
    #db_trends = dbclient['Twitter_Trends']
    print "here3"
    #db_coll = db_trends.Trends_Just_Rate
    db_coll = db_trends.Trends_Place_Rate
    print "here3"
    #hashtags = db_coll.find({}).distinct("Hashtag")
    dict_top = list(db_coll.find({}).sort([("Rate_Inc",-1)]).limit(50))
    #print dict_top
    #print "here3"
    #return a
    for tag in dict_top:
        dict_top3 = {}
        dict_top3.update({"name": tag["Hashtag"].replace(" ", "__")})
        #dict_top3.update({"score": int((tag["Rate_Inc"] + tag["Rate_Inc"]*random.random()))})
        vol_dict = tag["Vol_Dict"]
        score=0
        #print vol_dict
        for i in vol_dict:
            score = score + len(vol_dict[i])-1
        dict_top3.update({"score": score})
        dict_top3.update({"ri": round(tag["Rate_Inc"], 2)})
        a.append(dict_top3)
    print "DOne"
    #print dict_top
    return a


        
def hashtag(request,hasht):
    context_dict={}
    return render(request, 'app/hashtag.html', context_dict)
    
def autocompleteModel(request):
    if 'term' in request.GET:
        tags = Woeid.objects.filter(name__icontains=request.GET['term']).values_list('name',flat=True)[:5]
        return HttpResponse( json.dumps( [ tag for tag in tags ] ) )
    return HttpResponse()   
