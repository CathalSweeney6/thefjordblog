from . import views
from django.urls import path


urlpatterns = [
    path('', views.ArticleList.as_view(), name='home'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('like/<slug:slug>', views.ArticleLike.as_view(), name='article_like'),
    path('delete_user_comment/<int:comment_id>',
         views.delete_user_comment, name='delete_user_comment'),
    path('edit_user_comment/<int:pk>', views.EditComment.as_view(),
         name='edit_user_comment'),
    path('search', views.search, name='search'),
    path('contact', views.contact, name="contact"),
    path('success.html', views.success, name="success"),
    path('newsletter', views.newsletter, name="newsletter"),
    path('success_newsletter', views.success_newsletter, name="success_newsletter"),
]
