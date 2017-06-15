from pymongo import MongoClient
import os


def main():
	dbclient = MongoClient('mongodb://admin:admin@54.172.143.59:27017')
	db_trends = dbclient['Twitter_Trends']
	woeid1 = db_trends.woeids1
	woeid2 = db_trends.woeids2
	woeid3 = db_trends.woeids3
	db_woeid1 = list(woeid1.find({}))
	db_woeid2 = list(woeid2.find({}))
	db_woeid3 = list(woeid3.find({}))
	print("---------Woeid 1----------")
	for i in db_woeid1 :
		print i["name"]
	print("---------Woeid 2----------")
	for i in db_woeid2 :
		print i["name"]
	print("---------Woeid 3----------")
	for i in db_woeid3 :
		print i["name"]

if __name__ == '__main__':
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twtr.settings')
	from app.models import Woeid
	main()

