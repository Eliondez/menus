"""
URL configuration for menus_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rest_framework.authtoken import views as drf_views
from menu import views as menu_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/my_restaurant/', menu_views.UserRestaurantView.as_view()),
    path('api/client/menus/<int:menu_id>/', menu_views.MenuDetailView.as_view()),
    path('api/client/restaurants/<int:restaurant_id>/', menu_views.ClientRestaurantsView.as_view()),
    path('api/order_create/', menu_views.OrderCreate.as_view()),
    path('api/order/', menu_views.OrderDetail.as_view()),
]

urlpatterns += [
    path('api-token-auth/', drf_views.obtain_auth_token)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('auth/tokens/', users_views.TokensListView.as_view())]

