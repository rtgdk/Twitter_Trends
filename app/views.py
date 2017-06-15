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

from .models import Woeid
# Create your views here.

dbclient = MongoClient('mongodb://admin:admin@54.172.143.59:27017')
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
    context_dict["newt2"] = top_trends_fetch("India")
    context_dict["newt1"] = top_trends_fetch("Worldwide")
    context_dict["country2"] = "India"
    context_dict["country1"] = "Worldwide"
    context_dict["country3"] = "Worldwide"
    context_dict["country4"] = "India"
    context_dict['topr'] = fetch_top_risers2("Worldwide")
    context_dict['topr2'] = fetch_top_risers2("India")
    #context_dict["tweets"] = hlist
    # context_dict["volume"]= tvlist
    # context_dict["rate"]= rlist
    # context_dict["count"] = count
    return render(request, 'app/index.html', context_dict)


#from operator import itemgetter

# woeid = "India"
def top_trends_fetch(woeid):
    a=[]
    #return a
    #dbclient = MongoClient("mongodb://admin:admin@54.172.143.59:27017")
    #db_trends = dbclient['Twitter_Trends']
    db_coll_trends = db_trends.Trends_Place
    #db_coll_freq = db_trends.Trends_Freq
    dict_trends = db_coll_trends.find({"Name": woeid}).sort([('_id', -1)])
    print dict_trends
    dict_top1 = {}
    dict_top2 = {}
    #current_date = datetime.date.today()
    #a = []
    ul = []
    count = 0
    #db_coll = db_trends.Trends_Place_Rate
    db_coll_rate = db_trends.Trends_Rate
    for trend in dict_trends:
        if count > 100:
            break
        if (ul.count(trend['Hashtag'])==0):
            ul.append(trend['Hashtag'])
            count = count + 1
            #dict_freq = db_coll_freq.find({"Hashtag": trend['Hashtag']})
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
    return a
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

def fetch_top_risers2(woeid):
	db_coll = db_trends.Trends_Place
	db_coll_tr = db_trends.Trends_Rate
	list_tr = db_coll.find({"Name":woeid}).distinct("Hashtag")
	a=[]
	#return a
	print len(list_tr)
	d=list(db_coll_tr.find({}).sort("_id", -1))   # trends rate list
	#e=list(db_coll.find({}).sort("_id", -1))			# all trends list
	for i in list_tr:
		#print (i)
		try:	
			dict_top={}
			ri = list(filter(lambda person: person['Hashtag'] == i, d))[0]
			dict_top.update({"name":i.replace(" ", "__")})
			dict_top.update({"ri":round(ri["Rate_Increase"],2)})
			score = db_coll.find({"Hashtag":i}).distinct("Woeid")
			dict_top.update({"score": len(score)})
			a.append(dict_top)
	#		print "right"
		except:
	#		print "wrong"
			pass
	sorted_dict3 = sorted(a, key=lambda k: k['ri'], reverse=True)
	return sorted_dict3
		
def hashtag(request,hasht):
	context_dict={}
	return render(request, 'app/hashtag.html', context_dict)
	
def autocompleteModel(request):
    if 'term' in request.GET:
        tags = Woeid.objects.filter(name__icontains=request.GET['term']).values_list('name',flat=True)[:5]
        return HttpResponse( json.dumps( [ tag for tag in tags ] ) )
    return HttpResponse()	
	
"""
	for tag in hashtags:
		dict_top = list(db_coll.find({"Hashtag": tag}).sort([("_id", -1)]))
		length = len(dict_top)
		try:
			init_vol = dict_top[1]['Tweet_Volume']
			final_vol = dict_top[0]['Tweet_Volume']
			rate_increase = (float(float(final_vol - init_vol)/init_vol)) * 100
		except:
			rate_increase = 0.0
		dict_top3 = {}
		dict_top3.update({"name": tag.replace(" ", "__")})
		dict_top3.update({"score": dict_top[0]['Tweet_Volume']})
		dict_top3.update({"ri": round(rate_increase, 2)})
		a.append(dict_top3)
	dbclient.close()
	sorted_dict3 = sorted(a, key=lambda k: k['score'], reverse=True)
	b = sorted_dict3[0:100]
	return b
"""
"""
count = 0
for i in dict_top_risers:
    if (count > 1):
        break
    if i['Hashtag'] not in fetched:
        dict_top3 = {}
        fetched.append(i['Hashtag'])
        print i['Hashtag'], i['Rate_Increase']
        dict_top3.update({"name": i['Hashtag'].replace(" ", "__")})
        dict_top3.update({"score": i['Tweet_Volume']})
        dict_top3.update({"ri": round(i['Rate_Increase'], 2)})
        print dict_top3
        # print i['Hashtag']
        a.append(dict_top3)
        count = count + 1
    #print count
  
print ("hello")
print a
return a
"""  
# tweet_fetch("#IndiaontheRise", '10')


"""from Tkinter import *
import Tkinter
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

top = Tk()
L1 = Label(top, text="Trend")
L1.pack( side = TOP)
E1 = Entry(top, bd =5)

E1.pack(side = TOP)
top.geometry('200x200')

bs = StringVar()
df1 = pd.DataFrame()

def option_changed(*args):
    global df1
    df2 = df1[df1['Name'] == bs.get()]
    ser = pd.Series(df2['Tweet_Volume'])
    ser = ser.reset_index()
    a = df2['Timestamp'].values
    b = []
    for i in a:
        b.append(i[0:10] + " " + i[11:16])
    plt.xlabel('Time')
    plt.ylabel('Tweet Volume')
    plt.title(E1.get() + " at " + bs.get())
    plt.xticks(range(len(ser)), b, rotation=45)
    plt.rcParams["figure.figsize"] = [15, 10]
    plt.plot(ser['Tweet_Volume'])
    plt.show()


def helloCallBack():
    dbclient = MongoClient()
    db_trends = dbclient['Twitter_Trends']
    db_coll = db_trends.Trends_Place
    df = pd.DataFrame(list(db_coll.find()))
    global df1
    df1 = df[df['Hashtag'] == E1.get()]
    b = df1['Name'].values
    print len(b)
    b = b[0:20]
    bs.set(b[0])
    bs.trace("w", option_changed)
    bmenu = OptionMenu(top, bs, *b)
    bmenu.pack(side=TOP)

B = Tkinter.Button(top, text ="Get Locations", command = helloCallBack)

B.pack(side = TOP)

top.mainloop()"""
