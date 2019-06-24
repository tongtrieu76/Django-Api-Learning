from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list-user/', views.api_user_list, name="api_user_list"),
    path('login/', views.api_login, name="api_login"),

    # account user "pk"
    path('user/<int:pk>/', views.api_user_info, name="api_user_info"),

    # blog
    path('list-blog/', views.api_list_blog, name="api_blog_list"),
    path('blog/<int:id>/', views.api_one_blog, name="api_blog_id"),
    path('blog/<int:id>/vote/', views.api_one_blog_vote, name="api_blog_id_vote"),
    path('blog/new-blog/', views.api_new_blog, name="api_new_blog"),
]
urlpatterns = format_suffix_patterns(urlpatterns)