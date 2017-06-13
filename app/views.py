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
    """for i in cdict:
        tvlist = {}
        tvlist["hash"]=i['Hashtag']
        tvlist["tv"]=i['Tweet_Volume']
        tvlist["ri"]=math.ceil(i['Rate_Increase']*100)/100
        #count=count+1
        hlist.append(tvlist)
        #print i['Hashtag']"""
    context_dict["newt2"] = top_trends_fetch("India")
    context_dict["newt1"] = top_trends_fetch("Worldwide")
    context_dict["country2"] = "India"
    context_dict["country1"] = "Worldwide"
    context_dict["country3"] = "Top Risers"
    context_dict['topr'] = fetch_top_risers()
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
    db_coll_freq = db_trends.Trends_Freq
    dict_trends = db_coll_trends.find({"Name": woeid}).sort([('_id', -1)])
    print dict_trends
    dict_top1 = {}
    dict_top2 = {}
    current_date = datetime.date.today()
    a = []
    ul = []
    count = 0
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
            # print trend
            """if (dict_freq.count() == 0):
                score3 = float(trend['Tweet_Volume'] * 1)
                dict_top3.update({"name": trend['Hashtag'].replace(" ", "__")})
                dict_top3.update({"score": score3})
                dict_top3.update({"ri": round(trend['Rate_Increase'], 2)})
            else:
                for i in dict_freq:"""
            #score3 = float(trend['Tweet_Volume'])
            dict_top3.update({"name": trend['Hashtag'].replace(" ", "__")})
            dict_top3.update({"score": trend['Tweet_Volume']})
            dict_top3.update({"ri": trend['Tweet_Volume']})
            a.append(dict_top3)
        elif (ul.count(trend['Hashtag'])==1):
        		try:
		      		upd_tr = filter(lambda tw: tw['name'] == trend['Hashtag'], a)[0]
		      		ul.append(trend['Hashtag'])
		      		a.remove(upd_tr)
		      		final = upd_tr["ri"]
		      		init = trend["Tweet_Volume"]
		      		ri = ((final-init)/init)*100
		      		upd_tr.update({"ri":ri})
		      	except:
		      		pass
        else :
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
    response["timestamp"] = c
    response["tweetvol"] = d
    b = json.dumps(response)
    #print b
    return HttpResponse(b)
    #print b
    return HttpResponse(b,e,f)

def fetch_top_risers():
	a=[]
	return a
	#dbclient = MongoClient('mongodb://admin:admin@54.172.143.59:27017')
	#db_trends = dbclient['Twitter_Trends']
	db_coll = db_trends.Trends_Place
	hashtags = db_coll.find({}).distinct("Hashtag")
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
