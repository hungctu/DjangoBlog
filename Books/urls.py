from django.urls import path
from .views import (index,topic_list,category_list,book_category,book_topic,Book,book_author
                    ,chap,search,Rate)

urlpatterns = [
    path('',index.as_view(),name='index'),
    path('topic_list/',topic_list.as_view(),name='topic_list'),
    path('category_list/',category_list.as_view(),name='category_list'),
    path('book_category/<int:c_id>',book_category.as_view(),name='book_category'),
    path('book_topic/<int:t_id>',book_topic.as_view(),name='book_topic'),
    path('book/<int:ds_id>',Book.as_view(),name='book'),
    path('book_author/<int:tg_id>', book_author.as_view(), name='book_author'),
    path('chap/<int:ds_id>/<int:c_id>', chap.as_view(), name='chap'),
    path('search/', search.as_view(), name='search'),
    path('rating/<int:book_id>/<int:rating_type>', Rate.as_view(), name='rating'),
]