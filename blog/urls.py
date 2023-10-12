from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('search', views.search, name='search'),
    path('contact.html', views.contact, name="contact"),
    path('success.html', views.success, name="success"),
]
