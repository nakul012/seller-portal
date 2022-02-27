from django.urls import path

from portal.views import *

urlpatterns = [
   path('seller', SellerlistView.as_view()),
   path('seller/<int:pk>', SellerlistView.as_view()),
   path('platform', PlatformlistView.as_view()),
   path('user', UserlistView.as_view()),
   path('user/<int:pk>', UserlistView.as_view()),
   path('item', ItemlistView.as_view()),
   path('orderitem', OrderItemListView.as_view()),
   # Questions

   path('most-sold-item-via-platform', GetItemView.as_view()),

]


