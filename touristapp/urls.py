from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/authenticate', views.ApiAuthenticate, name='authenticate'),
    url(r'^api/create-user', views.CreateUser, name='create-user'),
    url(r'^api/create-travel-agency', views.CreateTravelAgency, name='create-travel-agency'),
    url(r'^api/add-spot', views.AddSpot, name='add-spot'),
    url(r'^api/create-package', views.CreatePackage, name='create-package'),
    url(r'^api/add-to-itinerary-details', views.AddSpotToPackage, name='add-spot-to-package'),
    url(r'^api/book-package', views.BookPackage, name='book-package'),
    url(r'^api/get-best-tours', views.GetBestTours, name='get-best-tours'),
    url(r'^api/get-featured-spots', views.GetFeaturedSpots, name='get-featured-spots'),
    url(r'^api/get-request-package-tg', views.GetRequestPackageTG, name='get-request-package-tg'),
    url(r'^api/confirm-by-tour-guide', views.ConfirmByTourGuide, name='confirm-by-tour-guide'),
    url(r'^add-new-package/', views.AddPackage, name='add-new-package'),
    url(r'^addpackageaccomodation.html', views.AddPackage, name='addpackageaccomodation.html'),
    url(r'^addpackagetransportation.html', views.AddPackage, name='addpackagetransportation.html'),
    url(r'^addpackageitinerary.html', views.AddPackage, name='addpackageitinerary.html'),
    url(r'^addpackageinclusion.html', views.AddPackage, name='addpackageinclusion.html'),
    url(r'^signin.html', views.SignIn, name='signin.html'),
    url(r'^signup.html', views.CreateTravelAgency, name='signup.html'),
    url(r'^api/get-booked-tours', views.GetBookedPackages, name='get-booked-tours'),
    url(r'^api/get-confirm-transaction', views.GetConfirmPackageTG, name='get-confirm-transaction'),
    url(r'^api/post-friends', views.PostFriends, name='post-friends'),
    url(r'^api/add-rating-to-tour-guide-and-package', views.AddRatingToTourGuideAndPackage, name='add-rating-to-tour-guide-and-package'),
    url(r'^api/get-friends-activity', views.GetFriendsActivity, name='get-friends-activity')
]