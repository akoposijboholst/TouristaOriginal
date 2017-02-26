from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
import uuid
import datetime
import MySQLdb
import mysql.connector
import constants
import json
import configs.settings
import requests
import urllib
import urllib2
import os
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.utils.translation import ugettext_lazy as _


dns = 'http://192.168.2.104:8000'
cnx = mysql.connector.connect(user='akoposijboholst', password='HouseBoholst16', host='127.0.0.1', database='tourista')
if cnx.is_connected():
	print "Successfully connected to MySql!"
	
@csrf_exempt
def index(request):
	return render(request, 'home.html')

def SignIn(request):
	return render(request, 'signin.html')

def LandingPage(request):
	view_tourpackages_statement = "select * from return_tour_packages order by rating desc limit 10;"

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	data = []

	try:
		cursor.execute(view_tourpackages_statement)
		for (packageID, packageName, description, payment, rating, numOfSpots, duration, travelAgencyId, agencyName) in cursor:
			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageID + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE) in cursorB:
				counter = ++counter
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})

			data.append({
				constants.RETURN_TOUR_PACKAGES[0]: packageID,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				constants.RETURN_TOUR_PACKAGES[2]: description,
				constants.RETURN_TOUR_PACKAGES[3]: payment,
				constants.RETURN_TOUR_PACKAGES[4]: 4,
				constants.RETURN_TOUR_PACKAGES[5]: counter,
				constants.RETURN_TOUR_PACKAGES[6]: 3,
				constants.RETURN_TOUR_PACKAGES[7]: travelAgencyId,
				constants.RETURN_TOUR_PACKAGES[8]: agencyName,
				constants.RETURN_TOUR_PACKAGES[9]: spot_data
			})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return 'lol'
	
	return render(request, 'landingpage.html', {'hehe':data})

def LandingPagePo():
	view_tourpackages_statement = "select * from return_tour_packages order by rating desc limit 10;"

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	data = []

	try:
		cursor.execute(view_tourpackages_statement)
		for (packageID, packageName, description, payment, rating, numOfSpots, duration, travelAgencyId, agencyName) in cursor:
			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageID + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE) in cursorB:
				counter = ++counter
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})

			data.append({
				constants.RETURN_TOUR_PACKAGES[0]: packageID,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				constants.RETURN_TOUR_PACKAGES[2]: description,
				constants.RETURN_TOUR_PACKAGES[3]: payment,
				constants.RETURN_TOUR_PACKAGES[4]: 4,
				constants.RETURN_TOUR_PACKAGES[5]: counter,
				constants.RETURN_TOUR_PACKAGES[6]: 3,
				constants.RETURN_TOUR_PACKAGES[7]: travelAgencyId,
				constants.RETURN_TOUR_PACKAGES[8]: agencyName,
				constants.RETURN_TOUR_PACKAGES[9]: spot_data
			})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return 'lol'
	
	return render(request, 'landingpage.html', {'hehe':data})

def AddPackage(request):

	if request.method == 'POST':
		param = request.path
		list_params = param.split('/')

		if 'addpackageaccomodation.html' in list_params:
			return render(request, 'addpackageaccomodation.html')

		elif 'addpackagetransportation.html' in list_params:
			return render(request, 'addpackagetransportation.html')

		elif 'addpackageitinerary.html' in list_params:
			return render(request, 'addpackageitinerary.html')

	return render(request, 'addpackageabout.html')

@csrf_exempt
def ApiAuthenticate(request):
	facebookId = ""
	userType = ""
	try:
		body = json.loads(request.body)
		print body
		facebookId = body['userId']
		userType = body['type']
	except Exception, e:
		userType = request.POST.get('type')

	statement = ""

	if userType == 'TG':
		statement = "SELECT * FROM TOUR_GUIDE_PROFILE WHERE facebookId = '" + facebookId + "';"; 

	elif userType == 'T':
		statement = "SELECT * FROM USER WHERE facebookId = '" + facebookId  + "';"

	elif userType == 'TA':
		email = request.POST.get('email')
		password = request.POST.get('password')
		statement = "SELECT * FROM travel_agency WHERE email = '" + email  + "' and password = '" + password + "';"

	cursor = cnx.cursor(buffered=True)
	cursorC = cnx.cursor(buffered=True)
	cursorD = cnx.cursor(buffered=True)
	data = {}

	try:
		cursor.execute(statement)

		if userType == 'TG':
			for (userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId, citizenship, photoUrl, guideId, ratings, PROFILE_DESCRIPTION, streetAddress, city, country, zipCode, province, priority, numAccept, numRequest) in cursor:
				card = {}
				cursorC.execute("SELECT accountNumber, cvv, expirationDate, creditCardEmail, creditCardPassword FROM card_details where userId='" + userId + "'")
				for (accountNumber, cvv, expirationDate, creditCardEmail, creditCardPassword) in cursorC:
					card = {
						"accountNumber": accountNumber, 
						"cvv":cvv, 
						"expirationDateYear":expirationDate.strftime('%Y'),
						"expirationDateMonth":expirationDate.strftime('%B'),
						"expirationDateDay":expirationDate.strftime('%d'), 
						"creditCardEmail":creditCardEmail, 
						"creditCardPassword":creditCardPassword
					}
				cursorD.execute("SELECT * from guide_avg_ratings where guideId='"+guideId+"';")
				rate = {}
				for(guideId, acts_professionaly, isknowledgeable, rightpersonality) in cursorD:
					rate = {
						"acts_professionaly":str(acts_professionaly),
						"isknowledgeable": str(isknowledgeable),
						"rightpersonality": str(rightpersonality)
					}
				data = {
					"userId": userId,
					"firstName":firstName,
					"lastName":lastName,
					"birthday":birthday.strftime('%Y-%m-%d'),
					"EMAIL":EMAIL,
					"contactNumber":contactNumber,
					"facebookId":facebookId,
					"citizenship": citizenship,
					"photoUrl": photoUrl,
					"guideId":guideId,
					"ratings":ratings,
					"PROFILE_DESCRIPTION":PROFILE_DESCRIPTION,
					"streetAddress":streetAddress,
					"city":city,
					"country":country,
					"zipCode":zipCode,
					"province":province,
					"priority":priority,
					"numAccept":numAccept,
					"numRequest": numRequest,
					"accountNumber": card["accountNumber"], 
					"cvv":card["cvv"], 
					"expirationDateYear":card["expirationDateYear"], 
					"expirationDateMonth":card["expirationDateMonth"], 
					"expirationDateDay":card["expirationDateDay"], 
					"creditCardEmail":card["creditCardEmail"], 
					"creditCardPassword":card["creditCardPassword"],
					"acts_professionaly": rate["acts_professionaly"],
					"isknowledgeable": rate["isknowledgeable"],
					"rightpersonality": rate["rightpersonality"]
				}
				cursorB = cnx.cursor(buffered=True)
				statement2 = "SELECT * FROM GUIDE_LANGUAGES WHERE guideId = '" + guideId + "';"
				cursorB.execute(statement2)
				data["language"] = []
				for (guideId, language) in cursorB:
					data["language"].append(language)

		elif userType == 'T':
			for (userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId) in cursor:
				data = {
					"userId": userId,
					"firstName":firstName,
					"lastName":lastName,
					"birthday":birthday.strftime('%Y-%m-%d'),
					"EMAIL":EMAIL,
					"contactNumber":contactNumber,
					"facebookId":facebookId
				}

		elif userType == 'TA':
			alert = 0
			for (travelAgencyId, agencyName, streetAddress, city, country, zipCode, contactNumber, email, password) in cursor:
				alert = 1
				data = {
					'travelAgencyId': travelAgencyId,
					'agencyName': agencyName,
					'streetAddress': streetAddress,
					'city': city,
					'country': country,
					'zipCode': zipCode,
					'contactNumber': contactNumber,
					'email': email
				}
			if alert == 0:
				return HttpResponse({'alert':alert})
			else:
				return HttpResponseRedirect('/landing/', {'alert': alert})


	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)
	return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def AddSpot(request):
	spot = json.loads(request.body)

	spotIdTemp = str(uuid.uuid4()).split("-")

	spotId = spotIdTemp[0]	
	spotName = spot[constants.SPOT[1]]
	streetAddress = spot[constants.SPOT[2]]
	city = spot[constants.SPOT[3]]
	country = spot[constants.SPOT[4]]
	zipCode = spot[constants.SPOT[5]]
	contactNumber = spot[constants.SPOT[6]]
	website = spot[constants.SPOT[7]]
	LONGTITUDE = spot[constants.SPOT[8]]
	LATITUDE = spot[constants.SPOT[9]]
	description = spot[constants.SPOT[11]]
	closing = spot[constants.SPOT[12]]
	opening = spot[constants.SPOT[13]]

	cursor = cnx.cursor(buffered=True)
	new_spot = (spotId, spotName, streetAddress, city, country, zipCode, contactNumber, website, LONGTITUDE, LATITUDE, description, closing, opening)
	insert_new_spot_statement = ("INSERT INTO SPOT"
								"("+constants.SPOT[0]+','+constants.SPOT[1]+','+constants.SPOT[2]+','+constants.SPOT[3]+','
								""+constants.SPOT[4]+','+constants.SPOT[5]+','+constants.SPOT[6]+','+constants.SPOT[7]+','
								""+constants.SPOT[8]+','+constants.SPOT[9]+','+constants.SPOT[11]+','+constants.SPOT[12]+','+constants.SPOT[13]+")"
								"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
								)

	try:
		cursor.execute(insert_new_spot_statement, new_spot)

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse('200')

@csrf_exempt
def CreatePackage(request):
	package = json.loads(request.body)

	packageIdTemp = str(uuid.uuid4()).split("-")

	packageId = packageIdTemp[0]
	packageName = package[constants.PACKAGE[1]]
	travelAgencyId = package[constants.PACKAGE[2]]
	payment = package[constants.PACKAGE[3]]
	numOfTGNeeded = package[constants.PACKAGE[4]]
	description = package[constants.PACKAGE[6]]
	minPeople = package[constants.PACKAGE[9]]

	cursor = cnx.cursor(buffered=True)
	new_package = (packageId, packageName, travelAgencyId, payment, numOfTGNeeded, rating, description, duration, numOfSpots, minPeople, photoFileName, photoPath)
	new_package_statement = ("INSERT INTO TOUR_PACKAGE"
							"("+constants.PACKAGE[0]+','+constants.PACKAGE[1]+','+constants.PACKAGE[2]+','
							""+constants.PACKAGE[3]+','+constants.PACKAGE[4]+','+constants.PACKAGE[5]+','
							""+constants.PACKAGE[6]+','+constants.PACKAGE[7]+','+constants.PACKAGE[8]+','
							""+constants.PACKAGE[9]+constants.PACKAGE[10]+','+constants.PACKAGE[11]+')'
							"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
							)

	try:
		cursor.execute(new_package_statement, new_package)

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse('200')

@csrf_exempt
def AddSpotToPackage(request):
	package = json.loads(request.body)
	packageType = package['type']
	table = ""
	if packageType == 'NON-CUSTOM':
		table = "ITINERARY_DETAILS"
	elif packageType == 'CUSTOM':
		table = "CUSTOM_ITINERARY_DETAILS"

	cursor = cnx.cursor(buffered=True)
	packageId = package[constants.ITINERARY_DETAILS[0]]
	spotId = package[constants.ITINERARY_DETAILS[1]]
	startTime = package[constants.ITINERARY_DETAILS[2]]
	description = package[constants.ITINERARY_DETAILS[3]]
	chronology = package[constants.ITINERARY_DETAILS[4]]
	endTime = package[constants.ITINERARY_DETAILS[5]]

	add_to_package = (packageId, spotId, startTime, description, chronology, endTime)
	add_to_package_statement = ("INSERT INTO "+table+" "+
									"("+constants.ITINERARY_DETAILS[0]+','+constants.ITINERARY_DETAILS[1]+','+constants.ITINERARY_DETAILS[2]+','
									""+constants.ITINERARY_DETAILS[3]+','+constants.ITINERARY_DETAILS[4]+','+constants.ITINERARY_DETAILS[5]+')'
									"VALUES (%s,%s,%s,%s,%s,%s)"
									)
	try:
		cursor.execute(add_to_package_statement, add_to_package)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse('200')

@csrf_exempt
def EditCustomPackage(request):
	package = json.loads(request.body)

	packageId = package['packageId']
	userId = package['userId']
	payment = package['payment']
	numOfTGNeeded = package['numOfTGNeeded']
	numOfSpots = package['numOfSpots']
	packageName = package[constants.PACKAGE[1]]
	description = package["description"]
	numOfDays = package["numOfDays"]
	itinerary_details = package["itinerary_details"]
	print description
	cursor = cnx.cursor(buffered=True)
	delete_package_statement = ("DELETE FROM CUSTOM_PACKAGE where packageId = '" + packageId + "'")
	new_package = (packageId, userId,payment,numOfTGNeeded,numOfSpots, packageName, description, numOfDays)
	new_package_statement = ("INSERT INTO CUSTOM_PACKAGE" +
							"(packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description, numOfDays)"+
							"VALUES (%s,%s,%s,%s,%s, %s, %s, %s)"
							)

	try:
		cursor.execute(delete_package_statement)
		cursor.execute(new_package_statement, new_package)

		for iti_d in itinerary_details:
			spotId = iti_d[constants.ITINERARY_DETAILS[1]]
			startTime = iti_d[constants.ITINERARY_DETAILS[2]]
			description2 = "ge"
			print description2
			chronology = iti_d[constants.ITINERARY_DETAILS[4]]
			endTime = iti_d[constants.ITINERARY_DETAILS[5]]

			add_to_package = (packageId, spotId, startTime, description2, chronology, endTime)
			add_to_package_statement = ("INSERT INTO CUSTOM_ITINERARY_DETAILS "+
											"("+constants.ITINERARY_DETAILS[0]+','+constants.ITINERARY_DETAILS[1]+','+constants.ITINERARY_DETAILS[2]+','
											""+constants.ITINERARY_DETAILS[3]+','+constants.ITINERARY_DETAILS[4]+','+constants.ITINERARY_DETAILS[5]+')'
											"VALUES (%s,%s,%s,%s,%s,%s)"
											)
			cursor.execute(add_to_package_statement, add_to_package)

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse('200')

@csrf_exempt
def DeleteSpot(request):
	package = json.loads(request.body)
	spotId = package['spotId']
	packageId = package['packageId']

	cursor = cnx.cursor(buffered=True)
	try:
		delete_spot_package_statement = "DELETE FROM CUSTOM_ITINERARY_DETAILS WHERE spotId = '" + spotId + "' and packageId = '" + packageId + "'"
		cursor.execute(delete_spot_package_statement)

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse('200')

@csrf_exempt
def CreateUser(request):
	user = json.loads(request.body)

	userId = user[constants.USER[0]]														#create random id
	firstName = user[constants.USER[1]]															#get firstName passed in mobile
	lastName = user[constants.USER[2]]															#get lastName passed in mobile
	date = datetime.datetime.strptime(user[constants.USER[3]], '%Y-%m-%d').date()				#get birthday and conver to date
	birthday = date.isoformat()																	#convert to date
	email = user[constants.USER[4]]																#get email passed in mobile
	contactNumber = user[constants.USER[5]]														#get contactNumber passed in mobile
	facebookId = user[constants.USER[6]]

	tour_guide = user["tourGuide"]																#used to check if create user is tour guide

	languages = user['languages']
	streetAddress = user['streetAddress']
	city = user['city']
	country = user['country']
	zipCode = user['zipCode']
	province = user['province']
	profile_description = user['PROFILE_DESCRIPTION']

	cursor = cnx.cursor(buffered=True)
	new_user = (userId, firstName, lastName, birthday, email, contactNumber, facebookId)
	insert_new_user_statement = ("INSERT INTO USER"
								"("+constants.USER[0]+','+constants.USER[1]+','+constants.USER[2]+','+constants.USER[3]+','+constants.USER[4]+','+constants.USER[5]+','+constants.USER[6]+")"
								"VALUES (%s, %s, %s, %s, %s, %s, %s)"
								)
	try:
		cursor.execute(insert_new_user_statement, new_user)
		if tour_guide == "True":
			new_tour_guide = ("TG-"+userId, userId, streetAddress, city, country, zipCode, province, profile_description, 10)
			insert_new_tour_guide_statement = ("INSERT INTO TOUR_GUIDE"
											"(guideId, userId, streetAddress, city, country, zipCode, province, profile_description, priority)"
											"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
											)

			cursor.execute(insert_new_tour_guide_statement, new_tour_guide)

			for lang in languages:
				insert_lang = ("INSERT INTO GUIDE_LANGUAGES"
								"(guideId, language)"
								"VALUES (%s, %s)"
							)

				values = ("TG-"+userId, lang)
				cursor.execute(insert_lang, values)

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse('200')

@csrf_exempt
def PostFriends(request):
	obj = json.loads(request.body)


	cursor = cnx.cursor(buffered=True)
	for obj2 in obj:
		value = (obj2[constants.USER[0]], obj2[constants.USER[6]])
		insert_friend = ("INSERT INTO FRIENDSHIP"
						"("+constants.USER[0]+","+constants.USER[6]+")"
						"VALUES (%s, %s)"
						)
		try:
			cursor.execute(insert_friend, value)
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			return HttpResponse(e)
		# print obj2

	cnx.commit()
	return HttpResponse("202")	

@csrf_exempt
def AddRatingToTourGuideAndPackage(request):
	obj = json.loads(request.body)

	guide_rating = obj['guide']
	package_rating = obj['package']

	cursor = cnx.cursor(buffered=True)
	for gr in guide_rating:
		value = (gr['guideId'], gr['acts_professionaly'], gr['isknowledgeable'], gr['rightpersonality'], gr['tourTransactionId'], gr['comments'])
		insert_guide_rating = ("INSERT INTO TOUR_GUIDE_RATING"
						"("+'guideId'+','+'acts_professionaly'+','+'isknowledgeable'+','+'rightpersonality'+','+'tourTransactionId'+','+'comments'+')'
						"VALUES (%s, %s, %s, %s, %s, %s)"
						)
		try:
			cursor.execute(insert_guide_rating, value)
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			return HttpResponse(e)

	value2 = (package_rating['packageId'], package_rating['rating'], package_rating['tourTransactionId'], package_rating['comments'])
	insert_package_rating = ("INSERT INTO TOUR_PACKAGE_RATING"
							"("+'packageId'+','+'rating'+','+'tourTransactionId'+','+'comments'+')'
							"VALUES (%s, %s, %s, %s)"
							)
	try:
		cursor.execute(insert_package_rating, value2)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse("202")	

@csrf_exempt
def CreateTravelAgency(request):

	if request.method == 'POST':
		travelagency = json.loads(request.body)

		travelAgencyIdTemp = str(uuid.uuid4()).split("-")
		travelAgencyId = travelAgencyIdTemp[0]

		agencyName = travelagency[constants.TRAVEL_AGENCY[1]]
		streetAddress = travelagency[constants.TRAVEL_AGENCY[2]]
		city = travelagency[constants.TRAVEL_AGENCY[3]]
		country = travelagency[constants.TRAVEL_AGENCY[4]]
		zipCode = travelagency[constants.TRAVEL_AGENCY[5]]
		contactNumber = travelagency[constants.TRAVEL_AGENCY[6]]
		email = travelagency[constants.TRAVEL_AGENCY[7]]

		path = configs.settings.BASE_DIR + "\\touristapp\static\\" + travelAgencyId
		os.makedirs(path)

		cursor = cnx.cursor(buffered=True)
		new_travel_agency = (travelAgencyId, agencyName, streetAddress, city, country, zipCode, contactNumber, email)
		insert_new_travel_agency_statement = ("INSERT INTO TRAVEL_AGENCY"
											"("+constants.TRAVEL_AGENCY[0]+","+constants.TRAVEL_AGENCY[1]+","+constants.TRAVEL_AGENCY[2]+","
											""+constants.TRAVEL_AGENCY[3]+","+constants.TRAVEL_AGENCY[4]+","+constants.TRAVEL_AGENCY[5]+","
											""+constants.TRAVEL_AGENCY[6]+","+constants.TRAVEL_AGENCY[7]+")"
											"VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
											)
		try:
			cursor.execute(insert_new_travel_agency_statement, new_travel_agency)
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			return HttpResponse(e)

		cnx.commit()
		return HttpResponse('200')

	elif request.method == 'GET':
		return render(request, 'sign-up.html')

@csrf_exempt
def BookPackage(request):
	bookpackage = json.loads(request.body)

	tourTransactionIdTemp = str(uuid.uuid4()).split("-")
	tourTransactionId = tourTransactionIdTemp[0]
	userId = bookpackage[constants.TOUR_TRANSACTION[1]]
	packageId = bookpackage[constants.TOUR_TRANSACTION[2]]
	reserveDate = (datetime.datetime.strptime(bookpackage[constants.TOUR_TRANSACTION[3]], '%Y-%m-%d').date()).isoformat()
	tourDate = (datetime.datetime.strptime(bookpackage[constants.TOUR_TRANSACTION[4]], '%Y-%m-%d').date()).isoformat()
	numOfPeople = bookpackage[constants.TOUR_TRANSACTION[5]]
	status = bookpackage[constants.TOUR_TRANSACTION[6]]
	bookType = bookpackage['type'] # CUSTOM OR NON-CUSTOM

	cursor = cnx.cursor(buffered=True)
	insert_new_tourtransaction_statement = ""
	new_tour_transaction = ""
	table = ""
	insert_language = ""
	if bookType == 'NON-CUSTOM':
		table = 'TOUR_TRANSACTION'
		insert_new_tourtransaction_statement = ("INSERT INTO " + table + " " +
				"(" + constants.TOUR_TRANSACTION[0]+
				"," + constants.TOUR_TRANSACTION[1]+
				"," + constants.TOUR_TRANSACTION[2]+
				"," + constants.TOUR_TRANSACTION[3]+
				"," + constants.TOUR_TRANSACTION[4]+
				"," + constants.TOUR_TRANSACTION[5]+
				"," + constants.TOUR_TRANSACTION[6]+
				") VALUES(%s,%s,%s,%s,%s,%s,%s)")
		assign_tg_statement = ("INSERT INTO GUIDE_PACKAGE VALUES(%s, %s)")
		new_tour_transaction=(tourTransactionId,userId,packageId,reserveDate,tourDate,numOfPeople,status)
		insert_language = ("INSERT INTO tour_transaction_language VALUES (%s, %s)")


	elif bookType == 'CUSTOM':
		table = 'TOUR_TRANSACTION_CUSTOM'
		insert_new_tourtransaction_statement = ("INSERT INTO " + table + " " +
				"(" + constants.TOUR_TRANSACTION[0]+
				"," + constants.TOUR_TRANSACTION[2]+
				"," + constants.TOUR_TRANSACTION[3]+
				"," + constants.TOUR_TRANSACTION[4]+
				"," + constants.TOUR_TRANSACTION[5]+
				"," + constants.TOUR_TRANSACTION[6]+
				") VALUES(%s,%s,%s,%s,%s,%s)")
		assign_tg_statement = ("INSERT INTO CUSTOM_GUIDE_PACKAGE VALUES(%s, %s)")
		new_tour_transaction=(tourTransactionId,packageId,reserveDate,tourDate,numOfPeople,status)
		insert_language = ("INSERT INTO tour_transaction_custom_languages VALUES (%s, %s)")

	
	assign_tg = (tourTransactionId,'TG-fqjGxEdbTRO8ufQRumkbaBk3Xg02')

	try:
		cursor.execute(insert_new_tourtransaction_statement,new_tour_transaction)
		cursor.execute(assign_tg_statement, assign_tg)
		for language in bookpackage['languages']:
			cursor.execute(insert_language, (tourTransactionId,language))

	except (MySQLdb.Error,MySQLdb.Warning) as e:
		return HttpResponse(e)
	cnx.commit()
	return HttpResponse("200")

def GetBookedPackages(request):
	userId = request.GET.get(constants.USER[0])
	status = request.GET.get(constants.TOUR_TRANSACTION[6])

	get_booked_packages_statement = "SELECT * FROM return_tourist_transaction_with_package_details WHERE userId='"+userId+"' AND status='"+status+"';"
	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	cursorC = cnx.cursor(buffered=True)

	get_custom_packages_statement = "SELECT * FROM return_custom_tour_transaction WHERE userId='"+userId+"' AND status='"+status+"';"
	cursor1 = cnx.cursor(buffered=True)
	cursor2 = cnx.cursor(buffered=True)
	cursor3 = cnx.cursor(buffered=True)

	data = []

	try:
		cursor.execute(get_booked_packages_statement)
		for (userId, tourTransactionId, packageId, packageName, reserveDate, tourDate, status, payment, description, rating, numOfSpots, duration, travelAgencyId, agencyName, photoFileName) in cursor:
			guide_details = []
			if status == 'Success':
				statement = "SELECT * from tour_guide_profile where guideId in (SELECT guideId from guide_package where tourTransactionId = '" + tourTransactionId + "');"
				cursorC.execute(statement)
				for (userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId, citizenship, photoUrl, guideId, ratings, PROFILE_DESCRIPTION, streetAddress, city, country, zipCode, province, priority, numAccept, numReject) in cursorC:
					guide_details.append({
						"userId": userId,
						"firstName":firstName,
						"lastName":lastName,
						"birthday":birthday.strftime('%Y-%m-%d'),
						"EMAIL":EMAIL,
						"contactNumber":contactNumber,
						"facebookId":facebookId,
						"guideId":guideId,
						"ratings":ratings,
						"PROFILE_DESCRIPTION":PROFILE_DESCRIPTION,
						"streetAddress":streetAddress,
						"city":city,
						"country":country,
						"zipCode":zipCode,
						"province":province,
						"priority":priority
					})


			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, description, chronology, endTime, spotName, LONGITUDE, LATITUDE) in cursorB:
				counter = ++counter
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})

			data.append({
				constants.RETURN_TOURIST_TRANSACTION[0]: userId,
				constants.RETURN_TOURIST_TRANSACTION[1]: tourTransactionId,
				constants.RETURN_TOURIST_TRANSACTION[2]: packageId,
				constants.RETURN_TOURIST_TRANSACTION[3]: packageName,
				constants.RETURN_TOURIST_TRANSACTION[4]: reserveDate.strftime('%Y-%m-%d'),
				constants.RETURN_TOURIST_TRANSACTION[5]: tourDate.strftime('%Y-%m-%d'),
				constants.RETURN_TOURIST_TRANSACTION[6]: status,
				constants.RETURN_TOURIST_TRANSACTION[7]: payment,
				constants.RETURN_TOUR_PACKAGES[9]: spot_data,
				"description": description,
				"rating": 0,
				"numOfSpots": counter,
				"duration": 0,
				"travelAgencyId": travelAgencyId,
				"agencyName": agencyName,
				"guideDetails": guide_details,
				"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoFileName
			})


		cursor1.execute(get_custom_packages_statement)
		for (packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description, numOfDays, tourTransactionId, reserveDate, tourDate, numOfPeople, status) in cursor1:
			print "PASOK"
			guide_details = []
			if status == 'Success':
				statement = "SELECT * from tour_guide_profile where guideId in (SELECT guideId from custom_guide_package where tourTransactionId = '" + tourTransactionId + "');"
				cursor3.execute(statement)
				for (userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId, citizenship, photoUrl, guideId, ratings, PROFILE_DESCRIPTION, streetAddress, city, country, zipCode, province, priority, numAccept, numReject) in cursor3:
					guide_details.append({
						"userId": userId,
						"firstName":firstName,
						"lastName":lastName,
						"birthday":birthday.strftime('%Y-%m-%d'),
						"EMAIL":EMAIL,
						"contactNumber":contactNumber,
						"facebookId":facebookId,
						"guideId":guideId,
						"ratings":ratings,
						"PROFILE_DESCRIPTION":PROFILE_DESCRIPTION,
						"streetAddress":streetAddress,
						"city":city,
						"country":country,
						"zipCode":zipCode,
						"province":province,
						"priority":priority
					})


			view_spot_itinerary_statement = "select * from return_custom_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursor2.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE) in cursor2:
				counter = ++counter
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})

			data.append({
				"tourTransactionId":tourTransactionId, #
				"userId":userId, #
				"reserveDate":reserveDate.strftime('%Y-%m-%d'), #
				"tourDate":tourDate.strftime('%Y-%m-%d'), #
				"numOfPeople":numOfPeople, 
				"status":status, #
				"packageId":packageId, #
				"payment":payment, #
				"numOfTGNeeded":numOfTGNeeded, 
				"numOfSpots":counter, 
				"description": description, #
				"rating": 0, #
				"duration": 0,
				"travelAgencyId": 0,
				"agencyName": "Me",
				"packageName":packageName,#
				constants.RETURN_TOUR_PACKAGES[9]: spot_data,#
				"guideDetails": guide_details
				# "photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoFileName
			})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cursor.close()
	cursorB.close()
	return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def ConfirmByTourGuide(request):
	confirm = json.loads(request.body)
	tourTransactionId = confirm[constants.TOUR_TRANSACTION[0]]
	guideId = confirm[constants.GUIDE_PACKAGE[1]]
	response = confirm['response']

	update_status_statement = "UPDATE TOUR_TRANSACTION SET status='"+response+"' WHERE tourTransactionId"+"='"+tourTransactionId+"';"
	cursor = cnx.cursor(buffered=True)

	try:
		cursor.execute(update_status_statement)
	except (MySQLdb.Error,MySQLdb.Warning) as e:
		return HttpResponse(e)
	cnx.commit()

	return HttpResponse("200")
	
def GetBestTours(request):
	view_tourpackages_statement = "select * from return_tour_packages order by rating desc limit 10;"

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	data = []

	try:
		cursor.execute(view_tourpackages_statement)
		for (packageID, packageName, description, payment, rating, numOfSpots, duration, travelAgencyId, agencyName, photoFileName) in cursor:
			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageID + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE) in cursorB:
				counter = ++counter
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})

			data.append({
				constants.RETURN_TOUR_PACKAGES[0]: packageID,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				constants.RETURN_TOUR_PACKAGES[2]: description,
				constants.RETURN_TOUR_PACKAGES[3]: payment,
				constants.RETURN_TOUR_PACKAGES[4]: 4,
				constants.RETURN_TOUR_PACKAGES[5]: counter,
				constants.RETURN_TOUR_PACKAGES[6]: 3,
				constants.RETURN_TOUR_PACKAGES[7]: travelAgencyId,
				constants.RETURN_TOUR_PACKAGES[8]: agencyName,
				constants.RETURN_TOUR_PACKAGES[9]: spot_data,
				"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoFileName
			})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cursor.close()
	cursorB.close()
	return HttpResponse(json.dumps(data), content_type="application/json")
	# return HttpResponse('200')

def GetFeaturedSpots(request):
	view_spots_statement = "select * from spot order by ratings desc limit 10;"

	cursor = cnx.cursor(buffered=True)
	data = []

	try:
		cursor.execute(view_spots_statement)
		for (spotId, spotName, streetAddress, city, country, contactNumber, website, LONGITUDE, LATITUDE, ratings, description, closing, opening, zipCode, price, photoFileName) in cursor:
				data.append({
					constants.SPOT[0]: spotId,
					constants.SPOT[1]: spotName,
					constants.SPOT[2]: streetAddress,
					constants.SPOT[3]: city,
					constants.SPOT[4]: country,
					constants.SPOT[5]: zipCode,
					constants.SPOT[6]: contactNumber,
					constants.SPOT[7]: website,
					constants.SPOT[8]: LONGITUDE,
					constants.SPOT[9]: LATITUDE,
					constants.SPOT[10]: ratings,
					constants.SPOT[11]: description,
					constants.SPOT[12]: closing,
					constants.SPOT[13]: opening,
					'price': price,
					'photoPath': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName
					})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	#kulang pani para makuha jud..

	return HttpResponse(json.dumps(data), content_type="application/json")

def GetTGPackage(request):
	guideId = request.GET.get('guideId')
	status = request.GET.get('status')
	view_requestpackage_tg = "SELECT * FROM RETURN_GUIDE_TRANSACTION WHERE guideId='" + guideId + "' AND status='" + status+"';"
	
	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)

	data = []
	try:
		cursor.execute(view_requestpackage_tg)
		for (tourTransactionId, userId, packageId, reserveDate, tourDate, numOfPeople, status, packageName, guideId, rating, photoFileName, travelAgencyId, agencyName, touristName, payment, numOfSpots, description) in cursor:

			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE) in cursorB:
				counter = counter + 1
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})
			data.append({
				constants.TOUR_TRANSACTION[0]: tourTransactionId,
				constants.TOUR_TRANSACTION[1]: userId,
				constants.TOUR_TRANSACTION[2]: packageId,
				constants.TOUR_TRANSACTION[3]: reserveDate.strftime('%Y-%m-%d'),
				constants.TOUR_TRANSACTION[4]: tourDate.strftime('%Y-%m-%d'),
				constants.TOUR_TRANSACTION[5]: numOfPeople,
				constants.TOUR_TRANSACTION[6]: status,
				constants.GUIDE_PACKAGE[1]: guideId,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				'rating': rating,
				'itinerary_details': spot_data,
				"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoFileName,
				"agencyName": agencyName,
				"touristName": touristName,
				"numOfSpots": counter,
				"price" :payment,
				"TGPayment": 0,
				"description": description
			})


	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cursor.close()
	return HttpResponse(json.dumps(data), content_type="application/json")

def GetFriendsActivity(request):
	userId = request.GET.get('userId')

	view_friends_activity = "select tourTransactionId, userId, packageId, reserveDate, max(tourDate), status, packageName from return_tourist_transaction where userId in (select userId from user where facebookId in (select facebookId from friendship where userId = '"+ userId+ "')) group by userId;"

	cursor = cnx.cursor(buffered=True)
	new_cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)

	data = []
	try:
		cursor.execute(view_friends_activity)
		for (tourTransactionId, userId, packageId, reserveDate, tourDate, status, packageName) in cursor:
			view_tour_package = "select * from return_tour_packages where packageId = '" + packageId + "';"
			new_cursor.execute(view_tour_package)

			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE) in cursorB:
				counter = ++counter
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})

			packagedata = []
			for (packageID, packageName, description, payment, rating, numOfSpots, duration, travelAgencyId, agencyName, photoFileName) in new_cursor:
				packagedata.append({
					constants.RETURN_TOUR_PACKAGES[0]: packageID,
					constants.RETURN_TOUR_PACKAGES[1]: packageName,
					constants.RETURN_TOUR_PACKAGES[2]: description,
					constants.RETURN_TOUR_PACKAGES[3]: payment,
					constants.RETURN_TOUR_PACKAGES[4]: 4,
					constants.RETURN_TOUR_PACKAGES[5]: counter,
					constants.RETURN_TOUR_PACKAGES[6]: 3,
					constants.RETURN_TOUR_PACKAGES[7]: travelAgencyId,
					constants.RETURN_TOUR_PACKAGES[8]: agencyName,
					constants.RETURN_TOUR_PACKAGES[9]: spot_data,
					"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoFileName
				})
			data.append({
				constants.TOUR_TRANSACTION[0]: tourTransactionId,
				constants.TOUR_TRANSACTION[1]: userId,
				constants.TOUR_TRANSACTION[2]: packageId,
				constants.TOUR_TRANSACTION[3]: reserveDate.strftime('%Y-%m-%d'),
				constants.TOUR_TRANSACTION[4]: tourDate.strftime('%Y-%m-%d'),
				constants.TOUR_TRANSACTION[6]: status,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				'package': packagedata
				})

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)
	
	return HttpResponse(json.dumps(data), content_type="application/json")

def GetImage(request):
	param = request.path
	list_params = param.split('/')
	image_path = ""
	if list_params[4] == 'package':
		pic, ext = os.path.splitext(list_params[6])
		image_path = "\\touristapp\static\\" + list_params[5] + "\\" + list_params[6]
	elif list_params[4] == 'spot':
		image_path = "\\touristapp\static\spots\\" + "\\" + list_params[6]
	path, ext = os.path.splitext(image_path)

	if ext == '.jpg':
		ext = 'jpg'
	elif ext == '.png':
		ext = 'png'
	content_type = "image/" + ext
	image_data = open(configs.settings.BASE_DIR + image_path, "rb").read()
	return HttpResponse(image_data, content_type=content_type)

@csrf_exempt
def CreateCustomPackage(request):
	package = json.loads(request.body)

	packageIdTemp = str(uuid.uuid4()).split("-")

	packageId = packageIdTemp[0]
	userId = package['userId']
	payment = 0
	numOfTGNeeded = package[constants.PACKAGE[4]]
	numOfSpots = 0
	packageName = package[constants.PACKAGE[1]]
	description = package["description"]
	numOfDays = package["numOfDays"]


	cursor = cnx.cursor(buffered=True)
	new_package = (packageId, userId,payment,numOfTGNeeded,numOfSpots, packageName, description, numOfDays)
	new_package_statement = ("INSERT INTO CUSTOM_PACKAGE"
							"(packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description, numOfDays)"
							"VALUES (%s,%s,%s,%s,%s, %s, %s, %s)"
							)

	try:
		cursor.execute(new_package_statement, new_package)

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse('200')

def GetCustomPackages(request):
	userId = request.GET.get('userId')
	statement = "SELECT * FROM CUSTOM_PACKAGE WHERE userId='"+userId+"';"

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	try:
		cursor.execute(statement)
		data = []
		for(packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description1, numOfDays) in cursor:
			view_spot_itinerary_statement = "select * from return_custom_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, description, chronology, endTime, spotName, LONGITUDE, LATITUDE) in cursorB:
				counter = ++counter
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})

			data.append({
				"packageId":packageId,
				"userId":userId,
				 "payment":payment, 
				 "numOfTGNeeded":numOfTGNeeded, 
				 "numOfSpots":numOfSpots, 
				 "packageName":packageName, 
				 "description":description1, 
				 "numOfDays":numOfDays,
				 "itinerary_details": spot_data
				})

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse(json.dumps(data), content_type="application/json")

def GetMyCustomPackageTransactions(request):
	userId = request.GET.get('userId')

	statement = "SELECT * FROM return_custom_tour_transaction WHERE userId = " + "'" + userId + "'"

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	try:
		cursor.execute(statement)
		custom_package = []
		for(packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description, numOfDays, tourTransactionId, reserveDate, tourDate, numOfPeople, status) in cursor:

			view_spot_itinerary_statement = "select * from return_custom_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE) in cursorB:
				counter = ++counter
				spot_data.append({
					constants.RETURN_SPOT_ITINERARY[0]: packageId,
					constants.RETURN_SPOT_ITINERARY[1]: spotId,
					constants.RETURN_SPOT_ITINERARY[2]: startTime,
					constants.RETURN_SPOT_ITINERARY[3]: description,
					constants.RETURN_SPOT_ITINERARY[4]: chronology,
					constants.RETURN_SPOT_ITINERARY[5]: spotName,
					constants.RETURN_SPOT_ITINERARY[6]: endTime,
					constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE
				})

			custom_package.append({
				'userId': userId,
				'tourTransactionId': tourTransactionId,
				'packageId': packageId,
				'packageName': packageName,
				'reserveDate': reserveDate.strftime('%Y-%m-%d'),
				'tourDate': tourDate.strftime('%Y-%m-%d'),
				'status': status,
				'payment': payment,
				'itinerary_details': spot_data
				})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse(json.dumps(custom_package), content_type="application/json")

def GetAllPackage(request):

	return HttpResponse(NotifyTourGuide())

def NotifyTourGuide():

	url = 'https://fcm.googleapis.com/fcm/send'
	values = {
		"to": "/topics/news",
		"data": {
			"notifType": "Booked",
			"userId": "4WsRc7IsriQIyuA7zraN24Cgcl12"
		},
		# ,
		"notification": {
			"title": "Successfully booked a trip!",
			"body": "Push"
		}
	}

	data = json.dumps(values)

	server_key = 'AAAAzfXo2LM:APA91bFZ6Adgvob0lEKkcv1NxEfDtZIhenSAYnmtqpADx_sJKxeYBSgygy_pYP03Pi643cVjHZsGq5SjGz26TOdqKsoI5SqKmN9vv96udPrV97TyVdKUHCCadOdqmaXmuvgf8OsV11gdtqQb_E9go_QZaXuLfuteMg'

	key = 'key='+server_key
	headers = {
		'Authorization':key,
		'Content-Type':'application/json'
	}

	# request = Request(url, urlencode(data).encode(), headers)
	# json = urlopen(request).read().decode()

	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	the_page = response.read()
	# response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=data)

	return 200

def ChooseTourGuide(city, language):
	statement = "select guideId from tour_guide where city = '" + city + "';"
	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)

	data = []
	try:
		cursor.execute(statement)
		for (guideId) in cursor:
			statement2 = "select"

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cursor.close()
	return HttpResponse(json.dumps(data), content_type="application/json")


def AddQRCode(request):
	qr = json.loads(request.body)

		

def ChooseTourGuide(request):
	location = 'Cebu'
	language = 'Filipino'
	statement = "select guideId from tour_guide_profile where city='" + location + "'))"
	statement2 = "(select guideId from guide_languages where language='" + language + "' and guideId in ("+statement
	final_statement = "select MAX((ratings*.5)+(numAccept*.5)), guideId from tour_guide where guideId in " + statement2
	print final_statement
	cursor = cnx.cursor(buffered=True)

	try:
		cursor.execute(final_statement)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	return HttpResponse("hihihi")
