# -*- coding: utf-8 -*-

#dependencies:
#https://github.com/facebook/facebook-python-business-sdk
#https://github.com/tqdm/tqdm

from facebookads.api import FacebookAdsApi
from facebookads.adobjects.targetingsearch import TargetingSearch
import time
from tqdm import *
import json



SLEEP_TIME = 60
MINIMUM_GLOBAL_AUDIENCE = 1000000

#Initialize a new Session and instantiate an API object: (add your information here)
my_app_id = 'your app id'
my_app_secret = 'your app secret'
my_access_token = 'your access token' 
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

interests = {}

#handle request error
def handle_error(interest_):
	number_tries = 0
	while number_tries<5:
		try:
			params = {
			    'type': 'adinterestsuggestion',
			    'interest_list': [interest_],
			}
			resp = TargetingSearch.search(params=params)
			return resp
		except:
			number_tries+=1
			time.sleep(SLEEP_TIME*number_tries)
	return None

#Get all possible interests to target with type=adTargetingCategory&class=interests
params = {
	'type': 'adTargetingCategory',
	'class': 'interests',
}

resp = TargetingSearch.search(params=params)

interestsCategoriesOld = {}
interestsCategoriesNew = {}
interests = {}
for x in resp:
	#keep only interest with audience bigger than 1M
	if x["audience_size"] > MINIMUM_GLOBAL_AUDIENCE:
		interests[x["id"]] = (x["name"],x["audience_size"])
		interestsCategoriesOld[x["id"]] = x["name"]

interestsCategoriesNew = interestsCategoriesOld.copy()

count = 0
errors = 0

#iterate until there is no new interest to be added
while len(interestsCategoriesNew)>0:
	interestsCategoriesOld = {}
	for x in tqdm(interestsCategoriesNew):
		#get suggestions
		params = {
		    'type': 'adinterestsuggestion',
		    'interest_list': [interestsCategoriesNew[x]],
		}
		try:
			resp = TargetingSearch.search(params=params)
			for y in resp:
				params = {
    				'type': 'adinterestvalid',
    				'interest_list': [y['name']]
				}
				resp2 = TargetingSearch.search(params=params)

				if y["id"] not in interests and resp2[0]["valid"] == True:
					if y["audience_size"] > MINIMUM_GLOBAL_AUDIENCE:
						interests[y["id"]] = (y["name"],y["audience_size"])
						interestsCategoriesOld[y["id"]] = y["name"]
		except:
			print "Request error...sleeping"
			time.sleep(SLEEP_TIME)
			print "Working again"
			resp = handle_error(interestsCategoriesNew[x])
			if resp != None:
				for y in resp:
					if y["id"] not in interests:
						if y["audience_size"] > MINIMUM_GLOBAL_AUDIENCE:
							interests[y["id"]] = (y["name"],y["audience_size"])
							interestsCategoriesOld[y["id"]] = y["name"]
	interestsCategoriesNew = interestsCategoriesOld.copy()

json.dump(interests,open("facebookDataInterests.txt","w"))
