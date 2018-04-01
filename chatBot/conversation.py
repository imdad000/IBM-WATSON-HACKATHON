import sys
import json
import watson_developer_cloud
import pywapi
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from math import sqrt
from random import seed
from random import randrange
from csv import reader
import datetime
from sklearn import datasets,linear_model

conversation = watson_developer_cloud.ConversationV1(
    username='e91c46f8-af25-4f34-8fef-2770b88a7ae6',
    password='kHshOoKQggLE',
    version='2018-03-08'
)

workspace_id = 'b1d807f3-080c-4b9a-bdee-dead8ed75a1b'

# 
# Simple linear Regression 
#
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

# Calculate the mean value of a list of numbers
def mean(values):
	return sum(values) / float(len(values))

# Calculate covariance between x and y
def covariance(x, mean_x, y, mean_y):
	covar = 0.0
	for i in range(len(x)):
		covar += (x[i] - mean_x) * (y[i] - mean_y)
	return covar

# Calculate the variance of a list of numbers
def variance(values, mean):
	return sum([(x-mean)**2 for x in values])

# Calculate coefficients
def coefficients(X,Y):
	x = X
	y = Y
	x_mean, y_mean = mean(X), mean(Y)
	b1 = covariance(X, x_mean, Y, y_mean) / variance(X, x_mean)
	b0 = y_mean - b1 * x_mean
	return [b0, b1]

# Simple linear regression algorithm
def simple_linear_regression(X,Y):
	b0, b1 = coefficients(X,Y)
	return [b0,b1]


location = 'Jabalpur'
cultivated_area = 5
current_crop = -1
irrigation_facilities = -1
season = 'whole year'
value = True

def loc(): # to be completed
	a = 'Delhi'
	return a

#
# Weather 
#

def probable_location(location_ID):
	count = 0
	loc_id = ""
	for possible_location in location_ID:
		count = count+1
		loc_id = possible_location
	#print (loc_id)
	if(count <= 1.0):
		return loc_id
	else:
		print ('There are number quite a few location with similar set of name, please be specific')
		for possible_location in location_ID:
			print(location_ID[possible_location])
			loc_id="-1"
		return loc_id

def weather_intent(chat):
	response = conversation.message(workspace_id=workspace_id, input={
	    'text': chat})
	if(location != -1): # location not available
		location_ID = pywapi.get_location_ids(location)
		loc_id = probable_location(location_ID)
		print (loc_id)
		if(loc_id != str(-1)):
			try:
				now = 'current_conditions'
				print (response)
				if(response['entities'] != []):
					for i in response['entities']:
						for j in i:
							if(j == 'entity' and i[j] == 'location'):
								location_ID = pywapi.get_location_ids(i['value'])
								print ('*')
								loc_id = probable_location(location_ID)
								if(loc_id == -1):
									return 0
							if(j == 'entity' and i[j] == 'time'):
								now = i['value']
					Weather_details = pywapi.get_weather_from_weather_com(loc_id)
					#print(Weather_details)
					if(now == 'current_conditions'):
						print ('It is '+Weather_details[now]['text']+' and '+Weather_details[now]['wind']['speed'] + 'Km/hr now in '+ Weather_details[now]['station'])
					else:
						overcast = 0
						for i in Weather_details:
							if(i == 'forecasts'):
								for j in Weather_details[i]:
									#print(j)
									for k in j:
										#print (now)
										#print (str(k) + str(j[k]))
										if(k == 'day_of_week' and j[k].lower() == now):
											# print ('*')
											print ('It is '+ j['day']['text'] + ' on ' + now)
										if(j['day']['text'] == 'overcast' or j['day']['text'] == 'storm'):
											overcast+=1

						if(overcast <= 1):
							print ('No need to worry, there are no overcast for this week')
						else:
							print ('There are quite a few chances for overcast, please be patient and calm')

					#if(response[])
					#print (Weather_details)
				else:
					Weather_details = pywapi.get_weather_from_weather_com(loc_id)
					print ('It is '+Weather_details[now]['text']+' and '+Weather_details[now]['wind']['speed'] + 'Km/hr now in '+ Weather_details[now]['station'])
			except:
				print ('Server seems busy, cannot display weather information. till then have cup of tea')

#
# Pesticide
#

def pesticide():
	print ('What is your pesticide Sprayer Output?')
	x = int(input())
	print(x*cultivated_area)

#
# Procedure
#

def valid_procedure():
	flag = 1
	if(season == str(-1)):
		print ('Please tell me the season, for which you want the predicition')
		print ('Kahrif, rabi or autumn')
		flag = 0
	elif(cultivated_area == -1):
		print ('For further calculation we need, how much area you have')
		flag = 0
	elif(location == -1):
		print ('what\'s your location, please share your location')
		flag=0
	return flag

def crop_forecasting():
	data = []
	data = load_csv('crop_production.csv')
	now = datetime.datetime.now()
	
	if(now.month >= 7 and now.month <= 10):
		season = 'kharif'
	elif(now.month >= 10 and now.month <= 11):
		season = 'autumn'
	elif((now.month >= 11 and now.month <= 12) or now.month <= 1):
		season = 'rabi'
	else:
		season = 'whole year'

	print (season)

	if(valid_procedure() == 1):
		print (str(season).lower() + " " + str(location).lower())
		Crop = {}
		for i in range(1,len(data)):
			#print (str(data[i][1]).lower() + " " + str(data[i][3]).lower())
			#print (data[i][3].lower() + " " + season.lower())
			#a = list(season.lower())
			#print (a)
			data[i][3] = str(data[i][3].lower())
			data[i][3] = data[i][3].strip()
			data[i][1] = str(data[i][1].lower())
			data[i][1] = data[i][1].strip()
			if(str(location.lower()) == data[i][1]  and season.lower() == data[i][3].lower()):	
				try:
					Crop[data[i][4]]=1
					# Production.append(float(data[i][6])/float(data[i][5]))
					# Year.append(data[i][2])
				except:
					continue
		print ('Here is a list of possible crop which can be grown with there approximate production on your cultivated area will be shown if possible')
		for i in Crop:
			Production = []
			Year = []
			for j in range(1,len(data)):
				data[j][3] = str(data[j][3].lower())
				data[j][3] = data[j][3].strip()
				data[j][1] = str(data[j][1].lower())
				data[j][1] = data[j][1].strip()
				if(str(location.lower()) == data[j][1]  and season.lower() == data[j][3].lower() and i == data[j][4]):	
					try:
						Production.append(float(data[j][6])/float(data[j][5]))
						Year.append(data[j][2])
					except:
						continue

			if(len(Year) == 0):
				print ('No dataset found for your location or region please try after some days')
			else:
				X = []
				for j in range(len(Year)):
					X.append(int(Year[j]))
				[float(j) for j in Production]
				# print (Production)
				# print (X)
				try:
					[b0,b1] = simple_linear_regression(X,Production)
					current_year = now.year
					predicition = current_year*b1+b0
					if(float(predicition) == 0):
						continue
					print (i + " " +str(predicition))
				except:
					continue

def msp(crop):
	data = []
	data = load_csv('crops.csv')
	msp_cost = -1
	now = datetime.datetime.now()
	#print(data)
	for i in range(1,len(data)):
		if(data[i][0].lower() == crop.lower()):
			msp_cost = i
			break
	if(msp_cost == -1):
		print ('No data found for the crop, please try after some other crop')
	else:
		Year = []
		Price = []
		j = 1
		while(j < len(data[msp_cost])):
			Year.append(data[0][j])
			Price.append(data[msp_cost][j])
			j+=2

		X = []
		for j in Price:
			X.append(float(j))
		Y = []
		for j in Year:
			Y.append(int(j))
		# print (X)
		# print (Y)
		try:
			[b0,b1] = simple_linear_regression(Y,X)
			current_year = now.year
			#print (current_year)
			predicition = current_year*b1+b0
			#print (predicition)
			if(predicition <= 0):
				print ('Sorry! no prediction avialable')
			else:
				print ('Minimum selling price of '+ crop+ ' ' +str(predicition))
		except:
			print ('Sorry! no prediction avialable')
			return

def cost(chat):
	response = conversation.message(workspace_id=workspace_id, input={
	    'text': chat})
	crop_data = str(-1)
	if(response['entities'] != []):
		for i in response['entities']:
			for j in i:
				if(j == 'entity' and i[j] == 'crops'):
					crop_data = i['value']
		msp(crop_data)
	else:
		print ('Can you be more specific, for which crop you need cost')
	# data = []
	# data = load_csv('crop_production.csv')
	# msp_cost = []

	# print (response['entit'])	





def bye():
	print ('Hope, to see you again')

#
#	Message Type
#
def msg_type(chat,intent,values,entities,text):
	#print (json_output)
	if(intent == 'greetings'):
		print(text)
		return True
	elif(intent == 'weather'):
		#print (values)
		#print (entities)
		weather_intent(chat)
		return True
	elif(intent == 'crop_forecasting'):
		crop_forecasting()
		return True
	elif(intent == 'cost'):
		cost(chat)
		return True
	elif(intent == 'goodbyes'):
		bye()
		return False
	elif(intent == 'pesticide'):
		pesticide()

while(value):
	chat = input()
	response = conversation.message(workspace_id=workspace_id, input={
	    'text': chat})
	#response = json.dumps(response)
	#print (response)
	intent = []
	values = []
	entities = []
	text = []
	for i in response:
		if(str(i) == 'intents'):
			#print(i)
			for j in response[i]:
				for k in j: # add anything here
					if(k == 'intent'):
						intent.append(j[k])
					elif(k == 'entities'):
						print (j[k])
						entities.append(j[k])
					elif(k == 'values'):
						values.append(j[k])
					elif(k == 'text' and j == 'output'):
						text.append(j[k])
	for intents in intent:
		value = msg_type(chat,intents,values,entities,text)
		#(weather_intent(chat,values,entities))

	#print (response['intents']['intent'])
	#msg_type(response['intents']['intent'],response['output']['text'],chat)
	#print (msg)

	


