from django.urls import path
from .views import (Login,register,Logout,user_profile,user_update,change_pass,book_list_manage,
                    status_update,book_detail,add_chap,update_chap,add_book,update_book)

urlpatterns = [
    path('login/',Login.as_view(),name="login"),
    path('register/',register.as_view(),name="register"),
    path('logout/',Logout.as_view(),name="logout"),
    path('',user_profile.as_view(),name="user_profile"),
    path('user_update/<int:user_id>',user_update.as_view(),name="user_update"),
    path('change_pass/<int:user_id>',change_pass.as_view(),name="change_pass"),
    path('book_list_manage/<int:user_id>',book_list_manage.as_view(),name="book_list_manage"),
    path('status_update/<int:book_id>/<int:user_id>',status_update.as_view(),name="status_update"),
    path('book_detail/<int:book_id>',book_detail.as_view(),name="book_detail"),
    path('add_chap/<int:book_id>',add_chap.as_view(),name="add_chap"),
    path('update_chap/<int:book_id>/<int:chap_id>',update_chap.as_view(),name="update_chap"),
    path('add_book/<int:user_id>',add_book.as_view(),name="add_book"),
    path('update_book/<int:book_id>/<int:user_id>',update_book.as_view(),name="update_book"),
]