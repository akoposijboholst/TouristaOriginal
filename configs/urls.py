from django.conf.urls import include, url
from django.contrib import admin

import touristapp.views

urlpatterns = [
    url(r'^$', include('touristapp.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'api/authenticate', touristapp.views.ApiAuthenticate, name='authenticate'),
    url(r'^api/create-user', touristapp.views.CreateUser, name='create-user'),
    url(r'^api/create-travel-agency', touristapp.views.CreateTravelAgency, name='create-travel-agency'),
    url(r'^api/add-spot', touristapp.views.AddSpot, name='add-spot'),
    url(r'^api/create-package', touristapp.views.CreatePackage, name='create-package'),
    url(r'^api/add-to-itinerary-details', touristapp.views.AddSpotToPackage, name='add-spot-to-package'),
    url(r'^api/book-package', touristapp.views.BookPackage, name='book-package'),
    url(r'^api/get-best-tours', touristapp.views.GetBestTours, name='get-best-tours'),
    url(r'^api/get-featured-spots', touristapp.views.GetFeaturedSpots, name='get-featured-spots'),
    url(r'^api/get-request-package-tg', touristapp.views.GetRequestPackageTG, name='get-request-package-tg'),
    url(r'^api/confirm-by-tour-guide', touristapp.views.ConfirmByTourGuide, name='confirm-by-tour-guide'),
    url(r'^add-new-package', touristapp.views.AddPackage, name='add-new-package'),
    url(r'^addpackageaccomodation.html', touristapp.views.AddPackage, name='addpackageaccomodation.html'),
    url(r'^addpackagetransportation.html', touristapp.views.AddPackage, name='addpackagetransportation.html'),
    url(r'^addpackageitinerary.html', touristapp.views.AddPackage, name='addpackageitinerary.html'),
    url(r'^addpackageinclusion.html', touristapp.views.AddPackage, name='addpackageinclusion.html'),
    url(r'^signin.html', touristapp.views.SignIn, name='signin.html'),
    url(r'^signup.html', touristapp.views.CreateTravelAgency, name='signup.html'),
    url(r'^api/get-booked-tours', touristapp.views.GetBookedPackages, name='get-booked-tours'),
    url(r'^api/get-confirm-transaction', touristapp.views.GetConfirmPackageTG, name='get-confirm-transaction'),
    url(r'^api/post-friends', touristapp.views.PostFriends, name='post-friends'),
    url(r'^api/add-rating-to-tour-guide-and-package', touristapp.views.AddRatingToTourGuideAndPackage, name='add-rating-to-tour-guide-and-package'),
    url(r'^api/get-friends-activity', touristapp.views.GetFriendsActivity, name='get-friends-activity')
]