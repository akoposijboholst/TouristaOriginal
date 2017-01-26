SPOT = [
	'spotId',
	'spotName',
	'streetAddress',
	'city',
	'country',
	'zipCode',
	'contactNumber',
	'website',
	'LONGITUDE',
	'LATITUDE',
	'ratings',
	'description',
	'closing',
	'opening'
]

TRAVEL_AGENCY = [
	'travelAgencyId',
	'agencyName',
	'streetAddress',
	'city',
	'country',
	'zipCode',
	'contactNumber',
	'email'
]

PACKAGE = [
	'packageId',
	'packageName',
	TRAVEL_AGENCY[0],
	'payment',
	'numOfTGNeeded',
	'rating',
	'description',
	'duration',
	'numOfSpots',
	'minPeople'
]

USER = [
	'userId',
	'firstName',
	'lastName',
	'birthday',
	'email',
	'contactNumber',
	'facebookId'
]

TOUR_TRANSACTION = [
	'tourTransactionId',
	'userId',
	'packageId',
	'reserveDate',
	'tourDate',
	'numOfPeople',
	'status'
]

RETURN_TOUR_PACKAGES = [
	PACKAGE[0],
	PACKAGE[1],
	PACKAGE[6],
	PACKAGE[3],
	PACKAGE[5],
	PACKAGE[8],
	PACKAGE[7],
	TRAVEL_AGENCY[0],
	TRAVEL_AGENCY[1],
	'itineraries'
]

ITINERARY_DETAILS = [
	PACKAGE[0],
	SPOT[0],
	'startTime',
	'description',
	'chronology',
	'endTime'
]

RETURN_SPOT_ITINERARY = [
	PACKAGE[0],
	SPOT[0],
	ITINERARY_DETAILS[2],
	ITINERARY_DETAILS[3],
	ITINERARY_DETAILS[4],
	SPOT[1],
	ITINERARY_DETAILS[5],
	'LONGITUDE',
	'LATITUDE'
]

GUIDE_PACKAGE = [
	TOUR_TRANSACTION[0],
	'guideId'
]

RETURN_TOURIST_TRANSACTION = [
	'userId',
	'tourTransactionId',
	'packageId',
	'packageName',
	'reserveDate',
	'tourDate',
	'status',
	'payment'
]