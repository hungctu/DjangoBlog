from django.db.models import Prefetch, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from .models import book, category_book, topic_book, topic, category, chapter, comment, rating
from User.models import customer_user

qry1 = "SELECT b.* FROM books_book b, books_chapter c where b.id = c.book_id group by b.id order by sum(view_number) desc"

# Create your views here.
class index(View):
    def get(self, request):
        danhsach = book.objects.all().filter(status=1)
        tl_ds = category_book.objects.all()
        cd_ds = topic_book.objects.all()
        list = []
        for item in danhsach:
            chaps = chapter.objects.all().filter(book_id=item.id).order_by('date_create')
            last = chaps.last()
            list.append([item.id, last.date_create])

        dsach = {"ds": danhsach, "tl": tl_ds, "cd": cd_ds, "list": list}

        return render(request, 'Books/index.html', dsach)


class topic_list(View):
    def get(self, request):
        cd = topic.objects.all()
        cd_ds = topic_book.objects.all()
        list = []
        for item in cd:
            length = len([x for x in cd_ds if x.topic.id == item.id])
            list.append({"id": item.id, "topic_name": item.topic_name, "length": length})
        cdlist = {"cd": list}
        return render(request, 'Books/list_topic.html', cdlist)


class category_list(View):
    def get(self, request):
        tl = category.objects.all()
        tl_ds = category_book.objects.all()
        list = []
        for item in tl:
            length = len([x for x in tl_ds if x.category.id == item.id])
            list.append({"id": item.id, "category_name": item.category_name, "length": length})
        tllist = {"tl": list}
        return render(request, 'Books/list_category.html', tllist)


class book_category(View):
    def get(self, request, c_id):
        ca = category.objects.get(pk=c_id)
        books = book.objects.all().prefetch_related(Prefetch('category_book_set')).filter(
            category_book__category_id=c_id, status=1)
        tl_ds = category_book.objects.all()
        cd_ds = topic_book.objects.all()

        list = []
        for item in books:
            chaps = chapter.objects.all().filter(book_id=item.id).order_by('date_create')
            last = chaps.last()
            list.append([item.id, last.date_create])

        dsach = {"books": books, "cd": cd_ds, "ca": ca, "tl": tl_ds, "list": list}
        return render(request, 'Books/book_category.html', dsach)


class book_topic(View):
    def get(self, request, t_id):
        to = topic.objects.get(pk=t_id)
        books = book.objects.all().prefetch_related(Prefetch('topic_book_set')).filter(topic_book__topic_id=t_id,
                                                                                       status=1)
        tl_ds = category_book.objects.all()
        cd_ds = topic_book.objects.all()

        list = []
        for item in books:
            chaps = chapter.objects.all().filter(book_id=item.id).order_by('date_create')
            last = chaps.last()
            list.append([item.id, last.date_create])

        dsach = {"books": books, "cd": cd_ds, "to": to, "tl": tl_ds, "list": list}
        return render(request, 'Books/book_topic.html', dsach)


class Book(View):
    def get(self, request, ds_id):
        ds = book.objects.get(pk=ds_id)
        tl_ds = category_book.objects.all()
        cd_ds = topic_book.objects.all()
        chap = chapter.objects.all().filter(book=ds_id).order_by('date_create')
        last = chap.last()
        first = chap.first()

        hot = book.objects.raw(qry1)
        view_number = chapter.objects.filter(book_id=ds_id).aggregate(Sum('view_number'))

        like = 0
        dislike = 0
        if rating.objects.filter(book_id=ds_id,rating_type=0).exists():
            like = len(rating.objects.all().filter(book_id=ds_id,rating_type=0))
        if rating.objects.filter(book_id=ds_id, rating_type=1).exists():
            dislike = len(rating.objects.all().filter(book_id=ds_id, rating_type=1))

        dausach = {"hot": hot, "ds": ds, "tl": tl_ds, "cd": cd_ds, "chap": chap, "first": first, "last": last,"like":like,"dislike":dislike,"view_number":view_number}
        return render(request, 'Books/book.html', dausach)

class Rate(View):
    def get(self,request,book_id,rating_type):
        if request.user.is_authenticated:
            user_id = request.user.id
            if rating.objects.filter(book_id=book_id,user_id=user_id).exists():
                rate = rating.objects.get(book_id=book_id,user_id=user_id)
                if rating_type != rate.rating_type:
                    rate.rating_type = rating_type
                else:
                    rate.rating_type = 2
            else:
                rate = rating(book_id=book_id, user_id=user_id,rating_type = rating_type)
            rate.save()

        return HttpResponseRedirect(reverse('book',args=[book_id]))

class book_author(View):
    def get(self, request, tg_id):
        author = customer_user.objects.get(pk=tg_id)
        books = book.objects.all().filter(user_id=tg_id)

        list = []
        for item in books:
            chap = chapter.objects.all().filter(book=item.id).order_by('-date_create').first()
            list.append({"id": item.id, "date": chap.date_create})

        tl_ds = category_book.objects.all()
        cd_ds = topic_book.objects.all()
        au = {"author": author, "books": books, "tl": tl_ds, "cd": cd_ds, "date": list}
        return render(request, 'Books/author.html', au)


class chap(View):
    def get(self, request, ds_id, c_id):
        ds = book.objects.get(pk=ds_id)
        hot = book.objects.raw(qry1)

        chaps = chapter.objects.all().filter(book_id=ds_id).order_by('id')
        first = chaps.first()
        last = chaps.last()
        curent_chap = chapter.objects.get(pk=c_id)
        curent_chap.view_number += 1
        curent_chap.save()
        comments = comment.objects.all().filter(chapter_id=c_id)

        index = list(chaps).index(curent_chap)
        last_index = list(chaps).index(last)
        prev = 0
        next = 0
        if index > 0:
            prev = chaps[index - 1]
        if index < last_index:
            next = chaps[index + 1]

        chapterl = {"ds": ds, "hot": hot, "chaps": chaps, "chap": curent_chap, "comments": comments, "first": first,
                    "last": last, "prev": prev, "next": next,"len":len(comments)}
        return render(request, "Books/chap.html", chapterl)
    def post(self,request,ds_id,c_id):
        if request.user.is_authenticated:
            user_id = request.user.id
            content = request.POST.get('comment-message')
            scomment = comment(chapter_id=c_id,user_id=user_id,content=content)
            scomment.save()
        return HttpResponseRedirect(reverse('chap', args=[ds_id,c_id]))

# class submit_comment(View):


class search(View):
    def post(self, request):
        print("Vào comment")
        pattern = request.POST.get('key')
        danhsach = book.objects.all().filter(status=1, book_name__contains=pattern)
        tl_ds = category_book.objects.all()
        cd_ds = topic_book.objects.all()

        dsach = {"ds": danhsach, "tl": tl_ds, "cd": cd_ds, "key": pattern}

        return render(request, 'Books/search.html', dsach)
