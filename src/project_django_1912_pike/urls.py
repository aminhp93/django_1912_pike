"""project_django_1912_pike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from .views import HomeView

from orders.views import OrderList, OrderDetail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^categories/', include('categories.urls', namespace='categories')),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^orders/$', OrderList.as_view(), name='order-list'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order-detail'),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^shopping/', include('shopping.urls', namespace='shopping')),
    url(r'^videos/', include('videos.urls', namespace='videos')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)