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
import forms
import base64

dns = 'http://192.168.254.104:8000'
cnx = mysql.connector.connect(user='akoposijboholst', password='HouseBoholst16', host='localhost', port="3306", database='tourista')
if cnx.is_connected():
	print "Successfully connected to MySql!"

@csrf_exempt
def index(request):
	return render(request, 'home.html')

def Login(request):
	return render(request, 'login-failed.html')

def SignIn(request):
	return render(request, 'signin.html')

def LandingPage(request):
	print request
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
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoPath) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoPath
				})

			data.append({
				constants.RETURN_TOUR_PACKAGES[0]: packageID,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				constants.RETURN_TOUR_PACKAGES[2]: description,
				constants.RETURN_TOUR_PACKAGES[3]: str(payment),
				constants.RETURN_TOUR_PACKAGES[4]: 4,
				constants.RETURN_TOUR_PACKAGES[5]: counter,
				constants.RETURN_TOUR_PACKAGES[6]: 3,
				constants.RETURN_TOUR_PACKAGES[7]: travelAgencyId,
				constants.RETURN_TOUR_PACKAGES[8]: agencyName,
				constants.RETURN_TOUR_PACKAGES[9]: spot_data
			})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return 'lol'

	cursor.close()
	cursorB.close()
	return render(request, 'landingpage.html', {'data':data})


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
	param = request.path
	print request.body
	list_params = param.split('/')

	facebookId = ""
	userType = ""
	email = ""
	password = ""
	try:
		body = json.loads(request.body)		
		print body
		userType = body['type']
		if userType == 'TA':
			email = body['email']
			password = body['password']
		else:
			facebookId = body['userId']


	except Exception, e:
		userType = request.POST.get('type')

	statement = ""

	if userType == 'TG':
		statement = "SELECT * FROM TOUR_GUIDE_PROFILE WHERE facebookId = '" + facebookId + "';"

	elif userType == 'T':
		statement = "SELECT * FROM USER WHERE facebookId = '" + facebookId  + "';"

	elif userType == 'TA':
		# email = request.POST.get('email')
		# password = request.POST.get('password')
		statement = "SELECT * FROM travel_agency WHERE email = '" + email  + "' and password = '" + password + "';"

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	cursorC = cnx.cursor(buffered=True)
	cursorD = cnx.cursor(buffered=True)
	data = {}

	try:
		cursor.execute(statement)

		if userType == 'TG':
			for (userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId, citizenship, photoUrl, guideId, ratings, PROFILE_DESCRIPTION, streetAddress, city, country, zipCode, province, priority, numAccept, numRequest, referal_points, verified) in cursor:
				card = {}
				cursorC.execute("SELECT accountNumber, cvv, expirationDate, creditCardEmail, creditCardPassword FROM card_details where userId='" + userId + "'")
				print "Shanyl Authenticate1"

				card = {
					"accountNumber": "To be added", 
					"cvv":"To be added", 
					"expirationDateYear":"1996",
					"expirationDateMonth":"02",
					"expirationDateDay":"23", 
					"creditCardEmail":email, 
					"creditCardPassword":"To be added"
						}
				for (accountNumber, cvv, expirationDate, creditCardEmail, creditCardPassword) in cursorC:
						card["accountNumber"] =  accountNumber
						card["cvv"] = cvv 
						card["expirationDateYear"] = expirationDate.strftime('%Y')
						card["expirationDateMonth"] = expirationDate.strftime('%B')
						card["expirationDateDay"] = expirationDate.strftime('%d') 
						card["creditCardEmail"] = creditCardEmail 
						card["creditCardPassword"] = creditCardPassword
				cursorD.execute("SELECT * from guide_avg_ratings where guideId='"+guideId+"';")
				rate = {}
				rate = {
						"acts_professionaly":str(0),
						"isknowledgeable": str(0),
						"rightpersonality": str(0)
					}
				for(guideId, acts_professionaly, isknowledgeable, rightpersonality) in cursorD:
						rate["acts_professionaly"] = str(acts_professionaly),
						rate["isknowledgeable"] = str(isknowledgeable),
						rate["rightpersonality"] = str(rightpersonality)
				print "Shanyl Authenticate3"

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
					"ratings":str(ratings),
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
					"rightpersonality": rate["rightpersonality"],
					"referal_points": str(referal_points),
					"verified": verified
				}
				print "Shanyl Authenticate4"
				statement2 = "SELECT * FROM GUIDE_LANGUAGES WHERE guideId = '" + guideId + "';"
				cursorB.execute(statement2)
				data["language"] = []
				for (guideId, language) in cursorB:
					data["language"].append(language)

		elif userType == 'T':
			card = {}
			for (userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId, citizenship, photoUrl, firebaseInstanceIdToken, referal_points) in cursor:
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
				data = {
					"userId": userId,
					"firstName":firstName,
					"lastName":lastName,
					"birthday":birthday.strftime('%Y-%m-%d'),
					"EMAIL":EMAIL,
					"contactNumber":contactNumber,
					"facebookId":facebookId,
					"referal_points": str(referal_points),
					"card": card
				}
				print data

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
				data = "Email and password did not match!"

			print data

			# return HttpResponseRedirect('http://localhost:8000/landingpage')

			# return render(request, 'landingpage.html', {'data':json.dumps(data)})

			cursor.close()
			cursorB.close()
			cursorC.close()
			cursorD.close()

			return HttpResponse(json.dumps(data), content_type="application/json")


	
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)
	
	cnx.commit()
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
	# print package

	packageIdTemp = str(uuid.uuid4()).split("-")

	packageId = packageIdTemp[0]
	packageName = package[constants.PACKAGE[1]]
	travelAgencyId = package[constants.PACKAGE[2]]
	payment = float(package[constants.PACKAGE[3]])
	numOfTGNeeded = int(package[constants.PACKAGE[4]])
	description = package[constants.PACKAGE[6]]
	minPeople = int(package[constants.PACKAGE[9]])
	imagebase64 = package["image"]
	# category = package["category"]
	duration = int(package["numOfDays"])

	imgdata = base64.b64decode(imagebase64+"==")
	print 1
	filename = 'touristapp/static/' + travelAgencyId + '/' + packageId + ".png"
	file = packageId + ".png"
	print 2
	with open(filename, 'wb') as f:
		f.write(imgdata)

	print 3
	cursor = cnx.cursor(buffered=True)
	new_package = (packageId, packageName, travelAgencyId, payment, numOfTGNeeded, 0.0, description, duration, 0, minPeople, file, "Family Tours", 0)
	new_package_statement = ("INSERT INTO TOUR_PACKAGE " +
							"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
							)
	print new_package

	try:
		cursor.execute(new_package_statement, new_package)
		print cursor
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		print e 
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

	print package
	cursor = cnx.cursor(buffered=True)
	packageId = package[constants.ITINERARY_DETAILS[0]]
	spotId = package[constants.ITINERARY_DETAILS[1]]
	startTime = package[constants.ITINERARY_DETAILS[2]]
	description = package[constants.ITINERARY_DETAILS[3]]
	endTime = package[constants.ITINERARY_DETAILS[5]]

	add_to_package = (packageId, spotId, startTime, description, endTime)
	add_to_package_statement = ("INSERT INTO "+table+" "+
									"("+constants.ITINERARY_DETAILS[0]+','+constants.ITINERARY_DETAILS[1]+','+constants.ITINERARY_DETAILS[2]+','+
									""+constants.ITINERARY_DETAILS[3]+','+constants.ITINERARY_DETAILS[5]+')'
									"VALUES (%s,%s,%s,%s,%s)"
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
	print user

	userId = user[constants.USER[0]]														#create random id
	firstName = user[constants.USER[1]]															#get firstName passed in mobile
	lastName = user[constants.USER[2]]															#get lastName passed in mobile
	date = datetime.datetime.strptime(user[constants.USER[3]], '%Y-%m-%d').date()				#get birthday and conver to date
	birthday = date.isoformat()																	#convert to date
	email = user[constants.USER[4]]																#get email passed in mobile
	contactNumber = user[constants.USER[5]]														#get contactNumber passed in mobile
	facebookId = user[constants.USER[6]]
	photoUrl = user["photoUrl"]
	firebaseInstanceIdToken = user["firebaseInstanceIdToken"]
	print user

	tour_guide = user["tourGuide"]																#used to check if create user is tour guide
	citizenship = user["citizenship"]
	languages = []
	streetAddress = ""
	city = ""
	country = ""
	zipCode = ""
	province = ""
	profile_description = ""
	guideId = ""
	
	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	new_user = (userId, firstName, lastName, birthday, email, contactNumber, facebookId, citizenship, photoUrl, firebaseInstanceIdToken,10)
	insert_new_user_statement = ("INSERT INTO USER"+
								# "("+constants.USER[0]+','+constants.USER[1]+','+constants.USER[2]+','+constants.USER[3]+','+constants.USER[4]+','+constants.USER[5]+','+constants.USER[6]+")"
								"(userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId, citizenship, photoUrl, firebaseInstanceIdToken, referal_points)"+
								"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
								)
	try:
		cursor.execute(insert_new_user_statement, new_user)
		if tour_guide == "True":
			languages = user['languages']
			streetAddress = user['streetAddress']
			city = user['city']
			country = user['country']
			zipCode = user['zipCode']
			province = user['province']
			profile_description = user['PROFILE_DESCRIPTION']
			guideId = "TG-"+userId
			new_tour_guide = (userId, guideId, 0,  profile_description, streetAddress, city, country, zipCode, province,10, 0, 0, 10, "NOT-VERIFIED")
			insert_new_tour_guide_statement = ("INSERT INTO TOUR_GUIDE"
											"(userId, guideId, ratings,profile_description, streetAddress, city, country, zipCode, province, priority, numAccept, numRequest, referal_points, verified)"
											"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
											)

			cursor.execute(insert_new_tour_guide_statement, new_tour_guide)

			for lang in languages:
				insert_lang = ("INSERT INTO GUIDE_LANGUAGES"
								"(guideId, language)"
								"VALUES (%s, %s)"
							)

				values = ("TG-"+userId, lang)
				cursorB.execute(insert_lang, values)


		cnx.commit()
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		print "juheue"
		return HttpResponse(e)

	except Exception as inst:
		print inst
		return HttpResponse(inst);

	data = {}
	if tour_guide == "True":
		card = {
			"accountNumber": "To be added", 
			"cvv":"To be added", 
			"expirationDateYear":"1996",
			"expirationDateMonth":"02",
			"expirationDateDay":"23", 
			"creditCardEmail":email, 
			"creditCardPassword":"To be added"
				}

		print "boholst"
		rate = {
			"acts_professionaly":str(0.0),
			"isknowledgeable": str(0.0),
			"rightpersonality": str(0.0)
				}
		print "boholst1"
		data = {
			"userId": userId,
			"firstName":firstName,
			"lastName":lastName,
			"birthday":birthday,
			"EMAIL":email,
			"contactNumber":contactNumber,
			"facebookId":facebookId,
			"citizenship": citizenship,
			"photoUrl": photoUrl,
			"guideId":guideId,
			"ratings":str(0),
			"PROFILE_DESCRIPTION":profile_description,
			"streetAddress":streetAddress,
			"city":city,
			"country":country,
			"zipCode":zipCode,
			"province":province,
			"priority":10,
			"numAccept":0,
			"numRequest": 0,
			"accountNumber": card["accountNumber"], 
			"cvv":card["cvv"], 
			"expirationDateYear":card["expirationDateYear"], 
			"expirationDateMonth":card["expirationDateMonth"], 
			"expirationDateDay":card["expirationDateDay"], 
			"creditCardEmail":card["creditCardEmail"], 
			"creditCardPassword":card["creditCardPassword"],
			"acts_professionaly": rate["acts_professionaly"],
			"isknowledgeable": rate["isknowledgeable"],
			"rightpersonality": rate["rightpersonality"],
			"referal_points": str(0),
			"verified": "NOT-VERIFIED",
			"languages": languages
		}
		print "boholst3"
	elif tour_guide == "false":
		card = {
			"accountNumber": "To be added", 
			"cvv":"To be added", 
			"expirationDateYear":"1996",
			"expirationDateMonth":"02",
			"expirationDateDay":"23", 
			"creditCardEmail":email, 
			"creditCardPassword":"To be added"
				}
		data = {
			"userId": userId,
			"firstName":firstName,
			"lastName":lastName,
			"birthday":birthday,
			"EMAIL":email,
			"contactNumber":contactNumber,
			"facebookId":facebookId,
			"referal_points": str(10),
			"card": card
		}
	cursor.close()
	cursorB.close()
	print data
	return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def PostFriends(request):
	obj = json.loads(request.body)
	print obj
	size = int(obj["size"])


	cursor = cnx.cursor(buffered=True)
	for x in range(0,size-1):
		print obj[str(x)]
		# value = (obj2[constants.USER[0]], obj2[constants.USER[6]])
		# insert_friend = ("INSERT INTO FRIENDSHIP"
		# 				"("+constants.USER[0]+","+constants.USER[6]+")"
		# 				"VALUES (%s, %s)"
		# 				)
		# try:
		# 	cursor.execute(insert_friend, value)
		# 	print 1
		# except (MySQLdb.Error, MySQLdb.Warning) as e:
		# 	return HttpResponse(e)
		# print obj2

	cnx.commit()
	return HttpResponse("202")	

@csrf_exempt
def AddRatingToTourGuideAndPackage(request):
	obj = json.loads(request.body)

	guide_rating = obj['guide']
	package_rating = obj['package']
	packageType = obj['type']
	table = ""

	if packageType == 'NON-CUSTOM':
		table = 'TOUR_GUIDE_RATING'
	elif packageType == 'CUSTOM':
		table = 'CUSTOM_TOUR_GUIDE_RATING'

	cursor = cnx.cursor(buffered=True)
	for gr in guide_rating:
		print gr
		value = (gr['guideId'], gr['acts_professionaly'], gr['isknowledgeable'], gr['rightpersonality'], package_rating['tourTransactionId'], package_rating['comments'])
		insert_guide_rating = ("INSERT INTO " + table + " "
						"("+'guideId'+','+'acts_professionaly'+','+'isknowledgeable'+','+'rightpersonality'+','+'tourTransactionId'+','+'comments'+')'
						"VALUES (%s, %s, %s, %s, %s, %s)"
						)

		try:
			cursor.execute(insert_guide_rating, value)
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			return HttpResponse(e)

	insert_package_rating = "UPDATE TOUR_PACKAGE_RATING SET rating = " + package_rating['rating']
	try:
		cursor.execute(insert_package_rating)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse("200")

@csrf_exempt
def AddCommentToTransaction(request):
	obj = json.loads(request.body)
	packageType = obj['type']
	tourTransactionId = obj['tourTransactionId']
	comments = obj['comments']
	table = ""
	cursor = cnx.cursor(buffered=True)

	if packageType == 'NON-CUSTOM':
		table = 'TOUR_PACKAGE_RATING'
	elif packageType == 'CUSTOM':
		table = 'CUSTOM_TOUR_PACKAGE_RATING'

	statement = "INSERT INTO " + table + " VALUES (%s, %s, %s)"
	data = (0, tourTransactionId, comments)

	try:
		cursor.execute(statement, data)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)
	cnx.commit()
	return HttpResponse("200")

@csrf_exempt
def CreateTravelAgency(request):

	if request.method == 'POST':
		travelagency = json.loads(request.body)
		print travelagency

		travelAgencyIdTemp = str(uuid.uuid4()).split("-")
		travelAgencyId = travelAgencyIdTemp[0]

		agencyName = travelagency[constants.TRAVEL_AGENCY[1]]
		streetAddress = travelagency[constants.TRAVEL_AGENCY[2]]
		city = travelagency[constants.TRAVEL_AGENCY[3]]
		country = travelagency[constants.TRAVEL_AGENCY[4]]
		zipCode = travelagency[constants.TRAVEL_AGENCY[5]]
		contactNumber = travelagency[constants.TRAVEL_AGENCY[6]]
		email = travelagency[constants.TRAVEL_AGENCY[7]]
		password = travelagency["password"]

		path = configs.settings.BASE_DIR + "\\touristapp\static\\" + travelAgencyId
		os.makedirs(path)

		cursor = cnx.cursor(buffered=True)
		new_travel_agency = (travelAgencyId, agencyName, streetAddress, city, country, zipCode, contactNumber, email, password)
		insert_new_travel_agency_statement = ("INSERT INTO TRAVEL_AGENCY"
											"("+constants.TRAVEL_AGENCY[0]+","+constants.TRAVEL_AGENCY[1]+","+constants.TRAVEL_AGENCY[2]+","
											""+constants.TRAVEL_AGENCY[3]+","+constants.TRAVEL_AGENCY[4]+","+constants.TRAVEL_AGENCY[5]+","
											""+constants.TRAVEL_AGENCY[6]+","+constants.TRAVEL_AGENCY[7]+",password)"
											"VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s)"
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
	print bookpackage

	tourTransactionIdTemp = str(uuid.uuid4()).split("-")

	tourTransactionId = tourTransactionIdTemp[0]

	userId = bookpackage["userId"]
	packageId = bookpackage[constants.TOUR_TRANSACTION[2]]
	tempReserveDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	reserveDate = (datetime.datetime.strptime(tempReserveDate, '%Y-%m-%d %H:%M:%S').date()).isoformat()
	tourDate = (datetime.datetime.strptime(bookpackage["tourDate"], '%Y-%m-%d').date()).isoformat()
	numOfPeople = int(bookpackage["numOfPeople"])
	status = bookpackage["status"]
	bookType = bookpackage['type'] # CUSTOM OR NON-CUSTOM
	language = bookpackage['language']
	referal_points = float(bookpackage['referal_points'])

	cursor = cnx.cursor(buffered=True)
	insert_new_tourtransaction_statement = ""
	new_tour_transaction = ""
	table = ""
	the_city = ""
	insert_language = ""
	get_first_spot = ""
	province = ""

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
		print "nasulod2"
		# assign_tg_statement = ("INSERT INTO GUIDE_PACKAGE VALUES(%s, %s, %s)")
		new_tour_transaction=(tourTransactionId,userId,packageId,reserveDate,tourDate,numOfPeople,"Request")
		print "nasulod3"
		insert_language = ("INSERT INTO tour_transaction_language VALUES (%s, %s)")
		print "gwapo"
		# get_first_spot = ("SELECT city from return_spot_itinerary rsi, spot s where rsi.spotId = s.spotId and packageId = '" + packageId + "' and chronology = 1")
	
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
		assign_tg_statement = ("INSERT INTO CUSTOM_GUIDE_PACKAGE VALUES(%s, %s, %s)")
		new_tour_transaction=(tourTransactionId,packageId,reserveDate,tourDate,numOfPeople,status)
		# print new_tour_transaction
		insert_language = ("INSERT INTO tour_transaction_custom_languages VALUES (%s, %s)")
		get_first_spot = ("SELECT  city, province from return_custom_spot_itinerary rsi, spot s where rsi.spotId = s.spotId and packageId = '" + packageId + "' and chronology = 0")

	cursor2 = cnx.cursor(buffered=True)
	statement = "UPDATE USER SET REFERAL_POINTS = " + str(referal_points)
	print "nasulod4"

	try:
		cursor.execute(insert_new_tourtransaction_statement,new_tour_transaction)
		cursor.execute(insert_language, (tourTransactionId,language))
		print "hihi"
		if bookType == 'CUSTOM':
			cursor2.execute(get_first_spot)
			for (city, prov) in cursor2:
				the_city = city
				province = prov

			guideId = ChooseTourGuide(province, the_city, language)
			print guideId + "oglA"
			assign_tg = (tourTransactionId,guideId, 'Waiting')
			cursor.execute(statement)
			cursor.execute(assign_tg_statement, assign_tg)

			cursor.execute("SELECT firebaseInstanceIdToken from user where userId = (SELECT userId from tour_guide where guideId = '" + guideId + "')")
			NotifyTourGuide(cursor.fetchone())
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
			if status == 'Success' or status == 'Pending':
				statement = "SELECT * from tour_guide_profile where guideId in (SELECT guideId from guide_package where tourTransactionId = '" + tourTransactionId + "');"
				cursorC.execute(statement)
				for (userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId, citizenship, photoUrl, guideId, ratings, PROFILE_DESCRIPTION, streetAddress, city, country, zipCode, province, priority, numAccept, numReject, referal_points, verified) in cursorC:
					guide_details.append({
						"userId": userId,
						"firstName":firstName,
						"lastName":lastName,
						"birthday":birthday.strftime('%Y-%m-%d'),
						"EMAIL":EMAIL,
						"contactNumber":contactNumber,
						"facebookId":facebookId,
						"guideId":guideId,
						"ratings": str(ratings),
						"PROFILE_DESCRIPTION":PROFILE_DESCRIPTION,
						"streetAddress":streetAddress,
						"city":city,
						"country":country,
						"zipCode":zipCode,
						"province":province,
						"priority":priority,
						"photoPath": dns + "/api/get/image/package/a6f4fa26/34dd2f97.jpg"
					})


			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, description, chronology, endTime, spotName, LONGITUDE, LATITUDE, hours, photoPath) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoPath
				})

			data.append({
				constants.RETURN_TOURIST_TRANSACTION[0]: userId,
				constants.RETURN_TOURIST_TRANSACTION[1]: tourTransactionId,
				constants.RETURN_TOURIST_TRANSACTION[2]: packageId,
				constants.RETURN_TOURIST_TRANSACTION[3]: packageName,
				constants.RETURN_TOURIST_TRANSACTION[4]: reserveDate.strftime('%Y-%m-%d %H:%M:%S'),
				constants.RETURN_TOURIST_TRANSACTION[5]: tourDate.strftime('%Y-%m-%d'),
				constants.RETURN_TOURIST_TRANSACTION[6]: status,
				constants.RETURN_TOURIST_TRANSACTION[7]: str(payment),
				constants.RETURN_TOUR_PACKAGES[9]: spot_data,
				"description": description,
				"rating": str(rating),
				"numOfSpots": counter,
				"duration": 0,
				"travelAgencyId": travelAgencyId,
				"agencyName": agencyName,
				"guideDetails": guide_details,
				"type": "NON-CUSTOM",
				"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoFileName
			})


		cursor1.execute(get_custom_packages_statement)
		for (packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description, numOfDays, tourTransactionId, reserveDate, tourDate, numOfPeople, status, filename) in cursor1:
			guide_details = []
			if status == 'Success' or status == 'Pending':
				statement = "SELECT * from tour_guide_profile where guideId in (SELECT guideId from custom_guide_package where tourTransactionId = '" + tourTransactionId + "');"
				cursor3.execute(statement)
				for (userId, firstName, lastName, birthday, EMAIL, contactNumber, facebookId, citizenship, photoUrl, guideId, ratings, PROFILE_DESCRIPTION, streetAddress, city, country, zipCode, province, priority, numAccept, numReject, referal_points, verified) in cursor3:
					guide_details.append({
						"userId": userId,
						"firstName":firstName,
						"lastName":lastName,
						"birthday":birthday.strftime('%Y-%m-%d'),
						"EMAIL":EMAIL,
						"contactNumber":contactNumber,
						"facebookId":facebookId,
						"guideId":guideId,
						"ratings": str(ratings),
						"PROFILE_DESCRIPTION":PROFILE_DESCRIPTION,
						"streetAddress":streetAddress,
						"city":city,
						"country":country,
						"zipCode":zipCode,
						"province":province,
						"priority":priority,
						"photoPath": dns + "/api/get/image/package/a6f4fa26/34dd2f97.jpg"
					})


			view_spot_itinerary_statement = "select * from return_custom_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursor2.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoPath) in cursor2:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoPath
				})

			data.append({
				"tourTransactionId":tourTransactionId, #
				"userId":userId, #
				"reserveDate":reserveDate.strftime('%Y-%m-%d %H:%M:%S'), #
				"tourDate":tourDate.strftime('%Y-%m-%d'), #
				"numOfPeople":numOfPeople, 
				"status":status, #
				"packageId":packageId, #
				"payment":str(payment), #
				"numOfTGNeeded":numOfTGNeeded, 
				"numOfSpots":counter, 
				"description": description, #
				"rating": 0, #
				"duration": 0,
				"travelAgencyId": 0,
				"agencyName": "Me",
				"packageName":packageName,#
				constants.RETURN_TOUR_PACKAGES[9]: spot_data,#
				"guideDetails": guide_details,
				"photoPath": dns+"/api/get/image/image/package/custom/"+filename,
				"type": "CUSTOM"
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
	bookType = confirm['type']
	print confirm
	table = ""
	print confirm

	if bookType == 'NON-CUSTOM':
		table = "GUIDE_PACKAGE"
	elif bookType == 'CUSTOM':
		table = "CUSTOM_GUIDE_PACKAGE"


	update_status_statement = "UPDATE " + table +" SET response='"+response+"' WHERE tourTransactionId='"+tourTransactionId+"';"
	cursor = cnx.cursor(buffered=True)
	try:
		cursor.execute(update_status_statement)
		# get_decline = "SELECT guideId from guide_package RESPONSE = 'Decline' and tourTransactionId ='"+tourTransactionId +"'"
		# cursor.execute(get_decline)
		# print cursor
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
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoPath) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoPath 
				})

			data.append({
				constants.RETURN_TOUR_PACKAGES[0]: packageID,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				constants.RETURN_TOUR_PACKAGES[2]: description,
				constants.RETURN_TOUR_PACKAGES[3]: str(payment),
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
	cnx.commit()
	return HttpResponse(json.dumps(data), content_type="application/json")
	# return HttpResponse('200')

def GetFeaturedSpots(request):
	view_spots_statement = "select * from spot order by ratings desc limit 10;"
	print request.session

	cursor = cnx.cursor(buffered=True)
	data = []

	try:
		cursor.execute(view_spots_statement)
		for (spotId, spotName, streetAddress, city, country, contactNumber, website, LONGITUDE, LATITUDE, ratings, description, closing, opening, zipCode, price, photoFileName, hours, province) in cursor:
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
					constants.SPOT[10]: str(ratings),
					constants.SPOT[11]: description,
					constants.SPOT[12]: closing,
					constants.SPOT[13]: opening,
					'price': str(price),
					'photoPath': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName,
					'hours': str(hours),
					'province': province
					})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	#kulang pani para makuha jud..

	return HttpResponse(json.dumps(data), content_type="application/json")

def GetTGPackage(request):
	guideId = request.GET.get('guideId')
	status = request.GET.get('status')
	if status == 'TAaccepted':
		status = 'TAaccept'

	view_requestpackage_tg = "SELECT * FROM RETURN_GUIDE_TRANSACTION WHERE guideId='" + guideId + "' AND status='" + status+"' and RESPONSE not in ('Decline','Cancel');"
	view_requestpackage_tg_custom = "SELECT * FROM RETURN_CUSTOM_GUIDE_TRANSACTION WHERE guideId='" + guideId + "' AND status='" + status+"' and RESPONSE <> 'Decline';"
	
	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)

	data = []
	try:
		cursor.execute(view_requestpackage_tg)
		for (tourTransactionId, userId, packageId, reserveDate, tourDate, numOfPeople, status, packageName, guideId, rating, photoPath, travelAgencyId, agencyName, touristName, payment, numOfSpots, description, RESPONSE, tgpayment) in cursor:
			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoFileName) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName
				})
			data.append({
				constants.TOUR_TRANSACTION[0]: tourTransactionId,
				constants.TOUR_TRANSACTION[1]: userId,
				constants.TOUR_TRANSACTION[2]: packageId,
				constants.TOUR_TRANSACTION[3]: reserveDate.strftime('%Y-%m-%d %H:%M:%S'),
				constants.TOUR_TRANSACTION[4]: tourDate.strftime('%Y-%m-%d'),
				constants.TOUR_TRANSACTION[5]: numOfPeople,
				constants.TOUR_TRANSACTION[6]: status,
				constants.GUIDE_PACKAGE[1]: guideId,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				'rating': str(rating),
				'itinerary_details': spot_data,
				"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoPath,
				"agencyName": agencyName,
				"touristName": touristName,
				"numOfSpots": counter,
				"price" :str(payment),
				"TGPayment": str(tgpayment),
				"description": description,
				"type": "NON-CUSTOM"
			})

		cursor.execute(view_requestpackage_tg_custom)
		for(tourTransactionId,userId,packageId, reserveDate, tourDate, numOfPeople, status, packageName, guideId, touristName, payment, numOfSpots, description, response) in cursor:
			view_spot_itinerary_statement = "select * from return_custom_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)
			counter = 0
			spot_data = []
			for (packageId, spotId, startTime, description, chronology, endTime, spotName, LONGITUDE, LATITUDE, hours, photoFileName) in cursorB:
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
				constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
				'hours': str(hours),
				'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName
				})
			data.append({
				constants.TOUR_TRANSACTION[0]: tourTransactionId,
				constants.TOUR_TRANSACTION[1]: userId,
				constants.TOUR_TRANSACTION[2]: packageId,
				constants.TOUR_TRANSACTION[3]: reserveDate.strftime('%Y-%m-%d %H:%M:%S'),
				constants.TOUR_TRANSACTION[4]: tourDate.strftime('%Y-%m-%d'),
				constants.TOUR_TRANSACTION[5]: numOfPeople,
				constants.TOUR_TRANSACTION[6]: status,
				constants.GUIDE_PACKAGE[1]: guideId,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				'rating': str(rating),
				'itinerary_details': spot_data,
				"photoPath": dns + "/api/get/image/package/a6f4fa26/34dd2f97.jpg",
				"agencyName": agencyName,
				"touristName": touristName,
				"numOfSpots": counter,
				"price" :str(payment),
				"TGPayment": 0,
				"description": description,
				"type": "CUSTOM"
			})

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cursor.close()
	cursorB.close()
	cnx.commit()
	return HttpResponse(json.dumps(data), content_type="application/json")

def GetAgencyTransaction(request):
	agencyId = request.GET.get('agencyId')
	status = request.GET.get('status')
	view_requestpackage_tg = "SELECT * FROM RETURN_AGENCY_TRANSACTION WHERE travelAgencyId ='" + agencyId + "' AND status ='" + status+"';"

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)

	data = []
	try:
		cursor.execute(view_requestpackage_tg)
		for (tourTransactionId, userId, packageId, reserveDate, tourDate, numOfPeople, status, packageName, rating, photoPath, travelAgencyId, agencyName, touristName, payment, numOfSpots, description, tgpayment) in cursor:
			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoFileName) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName
				})
			data.append({
				constants.TOUR_TRANSACTION[0]: tourTransactionId,
				constants.TOUR_TRANSACTION[1]: userId,
				constants.TOUR_TRANSACTION[2]: packageId,
				constants.TOUR_TRANSACTION[3]: reserveDate.strftime('%Y-%m-%d %H:%M:%S'),
				constants.TOUR_TRANSACTION[4]: tourDate.strftime('%Y-%m-%d'),
				constants.TOUR_TRANSACTION[5]: numOfPeople,
				constants.TOUR_TRANSACTION[6]: status,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				'rating': str(rating),
				'itinerary_details': spot_data,
				"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoPath,
				"agencyName": agencyName,
				"touristName": touristName,
				"numOfSpots": counter,
				"price" :str(payment),
				"TGPayment": str(tgpayment),
				"description": description,
				"type": "NON-CUSTOM"
			})

		# cursor.execute(view_requestpackage_tg_custom)
		# for(tourTransactionId,userId,packageId, reserveDate, tourDate, numOfPeople, status, packageName, guideId, touristName, payment, numOfSpots, description, response) in cursor:
		# 	view_spot_itinerary_statement = "select * from return_custom_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
		# 	cursorB.execute(view_spot_itinerary_statement)
		# 	counter = 0
		# 	spot_data = []
		# 	for (packageId, spotId, startTime, description, chronology, endTime, spotName, LONGITUDE, LATITUDE, hours, photoFileName) in cursorB:
		# 		counter = counter + 1
		# 		spot_data.append({
		# 		constants.RETURN_SPOT_ITINERARY[0]: packageId,
		# 		constants.RETURN_SPOT_ITINERARY[1]: spotId,
		# 		constants.RETURN_SPOT_ITINERARY[2]: startTime,
		# 		constants.RETURN_SPOT_ITINERARY[3]: description,
		# 		constants.RETURN_SPOT_ITINERARY[4]: chronology,
		# 		constants.RETURN_SPOT_ITINERARY[5]: spotName,
		# 		constants.RETURN_SPOT_ITINERARY[6]: endTime,
		# 		constants.RETURN_SPOT_ITINERARY[7]: LONGITUDE,
		# 		constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
		# 		'hours': str(hours),
		# 		'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName
		# 		})
		# 	data.append({
		# 		constants.TOUR_TRANSACTION[0]: tourTransactionId,
		# 		constants.TOUR_TRANSACTION[1]: userId,
		# 		constants.TOUR_TRANSACTION[2]: packageId,
		# 		constants.TOUR_TRANSACTION[3]: reserveDate.strftime('%Y-%m-%d'),
		# 		constants.TOUR_TRANSACTION[4]: tourDate.strftime('%Y-%m-%d'),
		# 		constants.TOUR_TRANSACTION[5]: numOfPeople,
		# 		constants.TOUR_TRANSACTION[6]: status,
		# 		constants.GUIDE_PACKAGE[1]: guideId,
		# 		constants.RETURN_TOUR_PACKAGES[1]: packageName,
		# 		'rating': str(rating),
		# 		'itinerary_details': spot_data,
		# 		"photoPath": dns + "/api/get/image/package/a6f4fa26/34dd2f97.jpg",
		# 		"agencyName": agencyName,
		# 		"touristName": touristName,
		# 		"numOfSpots": counter,
		# 		"price" :str(payment),
		# 		"TGPayment": 0,
		# 		"description": description,
		# 		"type": "CUSTOM"
		# 	})

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cursor.close()
	cursorB.close()
	cnx.commit()
	return HttpResponse(json.dumps(data), content_type="application/json")


def GetFriendsActivity(request):
	userId = request.GET.get('userId')

	view_friends_activity = "select tourTransactionId, rtt.userId, u.firstName, u.lastName, packageId, reserveDate, max(tourDate), status, packageName from return_tourist_transaction rtt, user u where rtt.userId = u.userId and rtt.userId in (select userId from user where facebookId in (select facebookId from friendship where userId = '"+ userId+ "')) group by userId;"

	cursor = cnx.cursor(buffered=True)
	new_cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)

	data = []
	try:
		cursor.execute(view_friends_activity)
		for (tourTransactionId, userId, firstName, lastName, packageId, reserveDate, tourDate, status, packageName) in cursor:
			view_tour_package = "select * from return_tour_packages where packageId = '" + packageId + "';"
			new_cursor.execute(view_tour_package)

			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoFileName) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName
				})

			packagedata = []
			for (packageID, packageName, description, payment, rating, numOfSpots, duration, travelAgencyId, agencyName, photoFileName) in new_cursor:
				packagedata.append({
					constants.RETURN_TOUR_PACKAGES[0]: packageID,
					constants.RETURN_TOUR_PACKAGES[1]: packageName,
					constants.RETURN_TOUR_PACKAGES[2]: description,
					constants.RETURN_TOUR_PACKAGES[3]: str(payment),
					constants.RETURN_TOUR_PACKAGES[4]: str(rating),
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
				"name": lastName + ", " + firstName,
				constants.TOUR_TRANSACTION[2]: packageId,
				constants.TOUR_TRANSACTION[3]: reserveDate.strftime('%Y-%m-%d %H:%M:%S'),
				constants.TOUR_TRANSACTION[4]: tourDate.strftime('%Y-%m-%d'),
				constants.TOUR_TRANSACTION[6]: status,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				'package': packagedata
				})

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

		print data
	
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
	imagebase64 = package["image"]
	imgdata = base64.b64decode(imagebase64+"==")
	filename = packageId + ".png" # I assume you have a way of picking unique filenames
	file = "touristapp/static/custom/" + filename
	with open(file, 'wb') as f:
		f.write(imgdata)

	print "pumasok si custom"
	cursor = cnx.cursor(buffered=True)
	new_package = (packageId, userId,payment,numOfTGNeeded,numOfSpots, packageName, description, numOfDays, filename)
	new_package_statement = ("INSERT INTO CUSTOM_PACKAGE"
							"(packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description, numOfDays, filename)"
							"VALUES (%s,%s,%s,%s,%s, %s, %s,%s,%s)"
							)

	try:
		print "pumasok si custom2"
		cursor.execute(new_package_statement, new_package)
		print "pumasok si custom3"

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
		for(packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description1, numOfDays, filename) in cursor:
			view_spot_itinerary_statement = "select * from return_custom_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, description, chronology, endTime, spotName, LONGITUDE, LATITUDE, hours, photoFileName) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName,
				})

				if filename == None:
					filename = "tourista_logo.png"

			data.append({
				"packageId":packageId,
				"userId":userId,
				 "payment":str(payment), 
				 "numOfTGNeeded":numOfTGNeeded, 
				 "numOfSpots":numOfSpots, 
				 "packageName":packageName, 
				 "description":description1, 
				 "numOfDays":numOfDays,
				 "photoPath": dns+"/api/get/image/image/package/custom/"+filename,
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
		for(packageId, userId, payment, numOfTGNeeded, numOfSpots, packageName, description, numOfDays, tourTransactionId, reserveDate, tourDate, numOfPeople, status, filename) in cursor:

			view_spot_itinerary_statement = "select * from return_custom_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoFileName) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName,
				})

			custom_package.append({
				'userId': userId,
				'tourTransactionId': tourTransactionId,
				'packageId': packageId,
				'packageName': packageName,
				'reserveDate': reserveDate.strftime('%Y-%m-%d %H:%M:%S'),
				'tourDate': tourDate.strftime('%Y-%m-%d'),
				'status': status,
				'payment': str(payment),
				 "photoPath": dns+"/api/get/image/image/package/custom/"+filename,
				'itinerary_details': spot_data
				})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse(json.dumps(custom_package), content_type="application/json")

# def GetAllPackage(request):

# 	return HttpResponse(NotifyTourGuide())

def ChooseTourGuide(province, city, language):
	# statement = "select guideId from tour_guide_profile where province = '"+ province + "' and city='" + city + "'))  group by guideId order by MAX((ratings*0.5)+(numAccept*0.5)) DESC LIMIT 0, 1"
	# statement2 = "(select guideId from guide_languages where language='" + language + "' and guideId in ("+statement
	# final_statement = "select MAX((ratings*0.5)+(numAccept*0.5)), guideId from tour_guide where guideId in " + statement2
	cursor = cnx.cursor(buffered=True)
	chosen = ""
	print province + " " + city + ' ' + language

	try:
		# cursor.execute(final_statement)
		# for guideId in cursor:
		# 	chosen = guideId[1]

		cursor.execute("SELECT guideId FROM TOUR_GUIDE_PROFILE WHERE province = '" + province + "' and city = '" + city + "' and verified = 'VERIFIED'")
		guide = []
		for guideId in cursor:
			guide.append(guideId[0])

		if len(guide)== 0:
			cursor.execute("SELECT guideId FROM TOUR_GUIDE_PROFILE WHERE province = '" + province + "' and verified = 'VERIFIED'")
			guidea = []

			for guideId in cursor:
				guidea.append(guideId[0])
		# 		counter1 = counter1 + 1

			if len(guidea) == 0:
				#invalidate user
				print "walang laman"

		elif len(guide) == 1:
			chosen = guide[0]
			return chosen

		elif len(guide) > 1:

			guide2 = []
			statement2 = "SELECT guideId from guide_languages where language = '" + language + "' and guideId in " + str(json.dumps(guide))
			statement2 = statement2.replace("[", "(")
			statement2 = statement2.replace("]", ")")
			print statement2
			cursor.execute(statement2)
			for guideId in cursor:
				print guideId[0]
				guide2.append(guideId[0])

			if len(guide2) == 0:
				statement3 = "select MAX((ratings*0.5)+(numAccept*0.5)), guideId from tour_guide where guideId in " + str(json.dumps(guide)) + " group by guideId order by MAX((ratings*0.5)+(numAccept*0.5)) DESC LIMIT 0, 1"
				print "bolstone"
				return getFinal(statement3)
			elif len(guide2) == 1:
				chose = guide2[0]
				return chose
			elif len(guide2) > 1:
				print str(json.dumps(guide2))
				statement3 = "select ((ratings*0.5)+(numAccept*0.5)), guideId from tour_guide where guideId in " + str(json.dumps(guide2)) + " group by guideId order by MAX((ratings*0.5)+(numAccept*0.5)) DESC LIMIT 0, 1"
				statement3 = statement3.replace("[", "(")
				statement3 = statement3.replace("]", ")")
				return getFinal(statement3)

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	return chosen

def getFinal(statement):
	print "Entered"
	cursor = cnx.cursor(buffered=True)
	try:
		cursor.execute(statement)
		yeah = cursor.fetchone()
		print yeah
		print yeah[1] + " kayata"
		return yeah[1]
			# return yass
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	return "hehe"


@csrf_exempt
def CancelBookedTransaction(request):
	body = json.loads(request.body)
	print body
	tourTransactionId = body['tourTransactionId']
	packageType = body['type']
	table = ""
	if packageType == 'CUSTOM':
		table = 'TOUR_TRANSACTION_CUSTOM'
	elif packageType == 'NON-CUSTOM':
		table = 'TOUR_TRANSACTION'

	cursor = cnx.cursor(buffered=True)
	statement = "UPDATE "+table + " SET status = 'Cancelled' where tourTransactionId = '" + tourTransactionId + "';"

	try:
		cursor.execute(statement)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse(200)

@csrf_exempt
def CancelTourGuide(request):
	body = json.loads(request.body)
	tourTransactionId = body['tourTransactionId']
	guideId = body['guideId']
	packageType = body['type']
	print body
	table = ""
	if packageType == 'CUSTOM':
		table = 'CUSTOM_GUIDE_PACKAGE'
	elif packageType == 'NON-CUSTOM':
		table = 'GUIDE_PACKAGE'

	print body

	cursor = cnx.cursor(buffered=True)
	statement = "UPDATE " + table + " SET RESPONSE = 'Cancel' where tourTransactionId = '" + tourTransactionId + "' and guideId = '" + guideId +"';"

	try:
		cursor.execute(statement)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cursor.close()
	cnx.commit()
	return HttpResponse(200)

@csrf_exempt
def AddQRCode(request):
	qr = json.loads(request.body)
	code_qr = qr['code_qr']
	discount = 500
	userId = qr['userId']

	cursor = cnx.cursor(buffered=True)
	statement = "INSERT INTO qr_code VALUES (%s, %s, %s)"
	data = (code_qr, discount, userId)

	try:
		cursor.execute(statement,data)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse(200)
	
@csrf_exempt
def UseQRCode(request):
	qr = json.loads(request.body)
	code_qr = qr['code_qr']
	userId = qr['userId']
	print qr

	cursor = cnx.cursor(buffered=True)
	statement = "SELECT COUNT(*) from claimed_qr_code where code_qr = '" + code_qr + "' and claimerUserId = '" + userId + "'"
	statement2 = "SELECT COUNT(*) from qr_code where code_qr = '" + code_qr + "'"
	statement4 = "SELECT REFERAL_POINTS from USER where userId = '" + userId + "'"

	data = {}

	try:
		cursor.execute(statement2)
		result = cursor.fetchone()
		existent = result[0]

		cursor.execute(statement4)
		rp = cursor.fetchone()

		if existent > 0:
			cursor.execute(statement)
			result2 = cursor.fetchone()
			number_of_rows = result2[0]

			if number_of_rows > 0:
				data = {
					"response": "QR Code already claimed",
					"referal_points": str(rp[0])
				}

				return HttpResponse(json.dumps(data), content_type="application/json")
			else:
				statement3 = "INSERT INTO CLAIMED_QR_CODE VALUES (%s ,%s)"
				cursor.execute(statement3, (code_qr, userId))
				cursor.execute(statement4)
				rp = cursor.fetchone()
				cnx.commit()
				data = {
					"response": "Success",
					"referal_points": str(rp[0])
				}
				return HttpResponse(json.dumps(data), content_type="application/json")
		else:
			data = {
				"response": "QR Code non-existent",
				"referal_points": str(rp[0])
			}
			return HttpResponse(json.dumps(data), content_type="application/json")
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

def RecommendPackageNumFriends(request):
	userId = request.GET.get('userId');


	statement = ("SELECT rtt.packageId, rtt.packageName, description, rtt.payment, rating, numOfSpots, duration, travelAgencyId, agencyName, rtt.photoFileName, COUNT(DISTINCT (userId)) as 'friendUser'"+ 
				"FROM return_tourist_transaction rtt, return_tour_package rtp WHERE rtt.packageId = rtp.packageId and userId IN "+
				"(SELECT userId FROM user WHERE facebookId IN "+
				"(SELECT facebookId FROM friendship WHERE userId = '" + userId + "')) GROUP BY packageId LIMIT 5")
	statement2 = "SELECT * "

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	data = []

	try:
		cursor.execute(statement)
		for (packageId, packageName, description, payment, rating, numOfSpots, duration, travelAgencyId, agencyName, photoFileName, friendUser) in cursor:
			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours,photoFileName) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName,
				})

			data.append({
				constants.RETURN_TOUR_PACKAGES[0]: packageId,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				constants.RETURN_TOUR_PACKAGES[2]: description,
				constants.RETURN_TOUR_PACKAGES[3]: str(payment),
				constants.RETURN_TOUR_PACKAGES[4]: 4,
				constants.RETURN_TOUR_PACKAGES[5]: counter,
				constants.RETURN_TOUR_PACKAGES[6]: 3,
				constants.RETURN_TOUR_PACKAGES[7]: travelAgencyId,
				constants.RETURN_TOUR_PACKAGES[8]: agencyName,
				constants.RETURN_TOUR_PACKAGES[9]: spot_data,
				"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoFileName,
				"numOfFriendsUser": friendUser
			})
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def EndTour(request):
	end = json.loads(request.body)
	tourTransactionId = end['tourTransactionId']
	guideId = end['guideId']
	bookType = end['type']
	table = ""
	print end

	if bookType == 'CUSTOM':
		table = "TOUR_TRANSACTION_CUSTOM"
	elif bookType == 'NON-CUSTOM':
		table = "TOUR_TRANSACTION"

	statement = "UPDATE " + table + " SET status = 'SUCCESS' where tourTransactionId = '" +  tourTransactionId + "'"
	cursor = cnx.cursor(buffered=True)

	try:
		cursor.execute(statement)
		return HttpResponse(200)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

def GetMBA(request):
	packageId = request.GET.get('packageId')

def GetAgencyPackage(request):
	packageId = request.GET.get('agencyId')

	statement = "SELECT * FROM TOUR_PACKAGE WHERE travelAgencyId = '" + packageId + "';"

	cursor = cnx.cursor(buffered=True)
	cursorB = cnx.cursor(buffered=True)
	data = []

	try:
		cursor.execute(statement)
		for (packageId, packageName, travelAgencyId, payment, numOfTGNeeded, rating, description, duration, numOfSpots, minPeople, photoFileName, category, tgpayment) in cursor:
			view_spot_itinerary_statement = "select * from return_spot_itinerary where packageId = '" + packageId + "' order by chronology asc"
			cursorB.execute(view_spot_itinerary_statement)

			counter = 0;
			spot_data = []
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoPath) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoPath
				})

			data.append({
				"packageId": packageId,
				"packageName": packageName,
				"travelAgencyId": travelAgencyId,
				"payment": str(payment),
				"numOfTGNeeded":numOfTGNeeded, 
				"rating": str(rating), 
				"description": description, 
				"duration": duration, 
				"numOfSpots": numOfSpots, 
				"minPeople": minPeople, 
				"photoPath": dns + "/api/get/image/package/" + travelAgencyId + "/" + photoFileName, 
				"category": category,
				"spots": spot_data,
				"tgpayment": str(tgpayment)
				})

		return HttpResponse(json.dumps(data), content_type="application/json")
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

def GetAllSpots(request):
	statement = "SELECT * FROM SPOT;"

	cursor = cnx.cursor(buffered=True)
	data = []

	try:
		cursor.execute(statement)
		for (spotId, spotName, streetAddress, city, country, contactNumber, website, LONGITUDE, LATITUDE, ratings, description, closing, opening, zipCode, price, photoFileName, hours, province) in cursor:
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
					constants.SPOT[10]: str(ratings),
					constants.SPOT[11]: description,
					constants.SPOT[12]: closing,
					constants.SPOT[13]: opening,
					'price': str(price),
					'photoPath': dns+"/api/get/image/spot/"+spotId+"/"+photoFileName,
					'hours': str(hours),
					'province': province
					})
		return HttpResponse(json.dumps(data), content_type="application/json")
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

def GetAllPackage(request):
	view_tourpackages_statement = "select * from return_tour_packages;"

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
			for (packageId, spotId, startTime, endTime, description, chronology, spotName, LONGITUDE, LATITUDE, hours, photoPath) in cursorB:
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
					constants.RETURN_SPOT_ITINERARY[8]:	LATITUDE,
					'hours': str(hours),
					'photoFileName': dns+"/api/get/image/spot/"+spotId+"/"+photoPath 
				})

			data.append({
				constants.RETURN_TOUR_PACKAGES[0]: packageID,
				constants.RETURN_TOUR_PACKAGES[1]: packageName,
				constants.RETURN_TOUR_PACKAGES[2]: description,
				constants.RETURN_TOUR_PACKAGES[3]: str(payment),
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
	cnx.commit()
	return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
def FirebaseInstance(request):
	kaya = json.loads(request.body)
	print kaya

	userId = kaya["userId"]
	firebaseInstanceIdToken = kaya["firebaseInstanceIdToken"]
	update_statement = "UPDATE USER SET firebaseInstanceIdToken = '"+firebaseInstanceIdToken + "' where userId = '" + userId + "'"
	cursor = cnx.cursor(buffered=True)
	try:
		cursor.execute(update_statement)
		cursor.close()
		cnx.commit()
		return HttpResponse(200)

	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

@csrf_exempt
def UpdatePackage(request):
	package = json.loads(request.body)

	packageId = package["packageId"]
	packageName = package[constants.PACKAGE[1]]
	travelAgencyId = package[constants.PACKAGE[2]]
	payment = float(package[constants.PACKAGE[3]])
	numOfTGNeeded = int(package[constants.PACKAGE[4]])
	description = package[constants.PACKAGE[6]]
	minPeople = int(package[constants.PACKAGE[9]])
	imagebase64 = package["image"]
	category = package["category"]
	tgpayment = float(package["tgpayment"])

	# imgdata = base64.b64decode(imagebase64)
	# filename = 'touristapp/static/' + travelAgencyId + '/' + packageId + ".png" # I assume you have a way of picking unique filenames
	# with open(filename, 'wb') as f:
	# 	f.write(imgdata)

	cursor = cnx.cursor(buffered=True)
	new_package = (packageId, packageName, travelAgencyId, payment, numOfTGNeeded, rating, description, duration, numOfSpots, minPeople, photoFileName, category, )
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
def UpdateSpotsPackage(request):
	packages = json.loads(request.body)
	print packages

	cursor = cnx.cursor(buffered=True)
	packageId = packages["packageId"]
	spotId = packages["spotId"]
	delete_spot_package_statement = "DELETE FROM ITINERARY_DETAILS WHERE PACKAGEID = '" + packageId + "' and spotId = '"+ spotId + "';"
	

	try:
		cursor.execute(delete_spot_package_statement)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		return HttpResponse(e)

	# for package in packages:
	# 	packageId = package[constants.ITINERARY_DETAILS[0]]
	# 	spotId = package[constants.ITINERARY_DETAILS[1]]
	# 	startTime = package[constants.ITINERARY_DETAILS[2]]
	# 	description = package[constants.ITINERARY_DETAILS[3]]
	# 	chronology = package[constants.ITINERARY_DETAILS[4]]
	# 	endTime = package[constants.ITINERARY_DETAILS[5]]

	# 	add_to_package = (packageId, spotId, startTime, description, chronology, endTime)
	# 	delete_spot_package_statement = ()
	# 	add_to_package_statement = ("INSERT INTO ITINERARY_DETAILS " +
	# 									"("+constants.ITINERARY_DETAILS[0]+','+constants.ITINERARY_DETAILS[1]+','+constants.ITINERARY_DETAILS[2]+','
	# 									""+constants.ITINERARY_DETAILS[3]+','+constants.ITINERARY_DETAILS[4]+','+constants.ITINERARY_DETAILS[5]+')'
	# 									"VALUES (%s,%s,%s,%s,%s,%s)"
	# 									)
	# 	try:
	# 		cursor.execute(add_to_package_statement, add_to_package)
	# 	except (MySQLdb.Error, MySQLdb.Warning) as e:
	# 		return HttpResponse(e)

	cnx.commit()
	return HttpResponse('200')

@csrf_exempt
def AcceptTravelRequest(request):
	confirm = json.loads(request.body)
	tourTransactionId = confirm[constants.TOUR_TRANSACTION[0]]
	response = confirm['response'] #TAaccept or TADecline
	bookType = confirm['type']
# 
	# "SELECT packageId from tour_transaction where tourTransaction"

	# get_first_spot = ("SELECT city from return_spot_itinerary rsi, spot s, tour_transaction tt where rsi.spotId = s.spotId and packageId = '" + packageId + "' and tt.tourTransactionId =  and chronology = 1")
	get_first_spot = "SELECT city, province FROM RETURN_SPOT_ITINERARY rsi, SPOT s WHERE rsi.spotId = s.spotId and rsi.packageId = (SELECT packageId from tour_transaction where tourTransactionId = '" + tourTransactionId + "')"
	assign_tg_statement = ("INSERT INTO GUIDE_PACKAGE VALUES(%s, %s, %s)")

	update_status_statement = ("UPDATE TOUR_TRANSACTION SET status = '"+response+"' WHERE tourTransactionId='"+tourTransactionId+"';")
	cursor = cnx.cursor(buffered=True)
	cursor2 = cnx.cursor(buffered=True)

	get_language = ("SELECT language FROM TOUR_TRANSACTION_LANGUAGE where tourTransactionId = '" + tourTransactionId + "'")

	the_city = ""
	province = ""
	lang = ""

	try:
		cursor.execute(update_status_statement)
		print "labas"
		if response == 'TAaccept':
			print "lumabas"
			assign_tg_statement = ("INSERT INTO GUIDE_PACKAGE VALUES(%s, %s, %s)")
			print "lalabas"
			cursor2.execute(get_first_spot)
			for (city, prov) in cursor2:
				the_city = city
				province = prov
			cursor.execute(get_language)
			lang = cursor.fetchone()

			print "ohla"
			guideId = ChooseTourGuide(province, the_city, lang[0])
			assign_tg = (tourTransactionId,guideId, 'Waiting')
			cursor.execute(assign_tg_statement, assign_tg)

			cursor.execute("SELECT firebaseInstanceIdToken from user where userId = (SELECT userId from tour_guide where guideId = '" + guideId + "')")
			# assign_tg = (tourTransactionId,"TG-fqjGxEdbTRO8ufQRumkbaBk3Xg02", 'Waiting')
			NotifyTourGuide(cursor.fetchone())
		elif response == 'TAdecline':
			# NotifyUser
			b = 1+1
	except (MySQLdb.Error,MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse("200")

@csrf_exempt
def DeletePackage(request):
	a = json.loads(request.body)
	print a

	packageId = a["packageId"]

	statement = "DELETE FROM TOUR_PACKAGE WHERE packageId = '" + packageId + "';"
	cursor = cnx.cursor(buffered=True)

	try:
		cursor.execute(statement)
	except (MySQLdb.Error,MySQLdb.Warning) as e:
		return HttpResponse(e)

	cnx.commit()
	return HttpResponse("200")

def NotifyTourGuide(firebaseInstanceIdToken):

	url = 'https://fcm.googleapis.com/fcm/send'
	values = {
		"to": '"' + firebaseInstanceIdToken[0] + '"',
		"data": {
			"notifType": "Booked",
			"userId": "4WsRc7IsriQIyuA7zraN24Cgcl12"
		},
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

def NotifyTourist(firebaseInstanceIdToken):

	url = 'https://fcm.googleapis.com/fcm/send'
	values = {
		"to": '"' + firebaseInstanceIdToken[0] + '"',
		"data": {
			"notifType": "Booked",
			"userId": "4WsRc7IsriQIyuA7zraN24Cgcl12"
		},
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

