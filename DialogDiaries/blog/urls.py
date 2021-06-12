from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.GetAllPosts.as_view(), name='home'),
    path('contactus/', views.ContactView.as_view(), name = 'contact'),
    path('about/', views.about, name = 'about'),
    path('create/', views.CreatePostView.as_view(), name='post_new'),
    path('sign-in/authenticate/', views.GetUserView.LogInUser, name='authenticate'),
    re_path('sign-in', views.GetSignIn.as_view(), name='sign_in'),
    path('sign-out/', views.GetUserView.LogOut, name='sign_out'),
    path('add-likes/', views.UpdatePost.AddLike, name='add_likes'),
    path('add-comments/', views.UpdatePost.AddComment, name='add_comments'),
    path('policy/', views.GetPolicy.as_view(), name='policy'),
    re_path('getallcategories/', views.getAllCategories, name='categories_list'),
    path('add-user-comments/', views.UpdatePost.AddUserComment, name='add_user_comments'),
    path('<slug:slug>/', views.GetPostDetails.PostDetails, name='post_detail'),
    path('<slug:slug>/', views.GetPostDetails.PostDetails, name='post_detail'),
    path('<slug:slug>/<str:showCommentBar>', views.GetPostDetails.PostDetailsComment, name='post_detail_comment'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/edit/<pk>', views.UpdatePostView.as_view(), name='update_post'),
    path('<pk>/profile/', views.UserProfileView.as_view(), name='userprofile'),
    path('<pk>/postUserProfile/', views.GetUserDetails.as_view(), name='post_user_profile'),
    path('search', views.search_post, name='search-post'),

]