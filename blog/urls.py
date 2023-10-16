from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('delete_user_comment/<int:comment_id>',
         views.delete_user_comment, name='delete_user_comment'),
    path('edit_user_comment/<int:pk>', views.EditComment.as_view(),
         name='edit_user_comment'),
    path('search', views.search, name='search'),
    path('contact.html', views.contact, name="contact"),
    path('success.html', views.success, name="success"),
    
]
