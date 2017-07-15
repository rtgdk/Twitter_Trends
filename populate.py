from pymongo import MongoClient
import os


def main():
	dbclient = MongoClient('mongodb://') # username:password@Ip:Port
	db_trends = dbclient['Twitter_Trends']
	print "here"
	woeid1 = db_trends.woeids1
	woeid2 = db_trends.woeids2
	woeid3 = db_trends.woeids3
	db_woeid1 = list(woeid1.find({}))
	print "here"
	db_woeid2 = list(woeid2.find({}))
	print "here"
	db_woeid3 = list(woeid3.find({}))
	print "here"
	print("---------Woeid 1----------")
	for i in db_woeid1 :
		print "here"
		Woeid.objects.get_or_create(name=i["name"])[0]
		print i["name"]
	print("---------Woeid 2----------")
	for i in db_woeid2 :
		Woeid.objects.get_or_create(name=i["name"])[0]
		print i["name"]
	print("---------Woeid 3----------")
	for i in db_woeid3 :
		Woeid.objects.get_or_create(name=i["name"])[0]
		print i["name"]

if __name__ == '__main__':
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twtr.settings')
	from app.models import Woeid
	main()

