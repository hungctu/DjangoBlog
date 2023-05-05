from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, decorators, logout
from Books.models import book, chapter, category_book, topic_book,category,topic
from Home.settings import logo_url, logoRoot
from .models import customer_user


# Create your views here.

class Login(View):
    def get(self, request):
        return render(request, 'User/Login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        my_user = authenticate(username=username, password=password)
        if my_user is None:
            return render(request, 'User/Login.html')
        login(request, my_user)
        return HttpResponseRedirect(reverse('index'))


class Logout(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('index'))


class register(View):
    def get(self, request):
        return render(request, "User/register.html")

    def post(self, request):
        username = request.POST.get('username')
        if not customer_user.objects.filter(username=username):
            image = 'images/user.png'
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = customer_user(fullname=fullname, user_image=image, email=email, username=username)
            user.set_password(password)
            user.save()
        return HttpResponseRedirect(reverse('login'))


class user_profile(View):
    def get(self, request):
        if request.user.is_authenticated:
            books = book.objects.all().filter(user_id=request.user.id)
            user = {"user": request.user, "len": len(list(books))}

            return render(request, 'User/userprofile.html', user)


class user_update(View):
    def post(self, request, user_id):
        user = customer_user.objects.get(pk=user_id)
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')

        user.fullname = fullname
        user.email = email
        if request.POST.get('user_image') != "":
            if request.FILES['user_image']:
                image = request.FILES['user_image']
                fs = FileSystemStorage(location=logoRoot, base_url=logo_url)
                filename = fs.save(image.name, image)
                uploaded_file_url = fs.url(filename)
                user.user_image = uploaded_file_url

        user.save()

        return HttpResponseRedirect(reverse('user_profile'))


class change_pass(View):
    def post(self, request, user_id):
        user = customer_user.objects.get(pk=user_id)
        cpass = request.POST.get('cpass')

        if check_password(cpass, user.password):
            npass = request.POST.get('newpass')
            user.set_password(npass)
            user.save()
        return HttpResponseRedirect(reverse('login'))


class book_list_manage(View):
    def get(self, request, user_id):
        books = book.objects.all().filter(user_id=user_id)
        list = []
        for item in books:
            chaps = chapter.objects.all().filter(book_id=item.id).order_by('date_create')
            # le = list(chaps)
            leng = len(chaps)
            last = chaps.last()
            list.append([item.id, leng, last.date_create])
        book_list = {"books": books, "id": id, "list": list}
        return render(request, 'User/book_list.html', book_list)


class status_update(View):
    def get(self, request, book_id, user_id):
        book1 = book.objects.get(pk=book_id)
        if book1.status == 1:
            book1.status = 0
        else:
            book1.status = 1
        book1.save()
        return HttpResponseRedirect(reverse('book_list_manage', args=[user_id]))


class book_detail(View):
    def get(self, request, book_id):
        book1 = book.objects.get(pk=book_id)
        tl_ds = category_book.objects.all()
        cd_ds = topic_book.objects.all()
        chaps = chapter.objects.all().filter(book=book_id).order_by('date_create')
        detail = {"book": book1, "tl": tl_ds, "cd": cd_ds, "chaps": chaps}
        return render(request, "User/book_detail.html", detail)


class add_chap(View):
    def get(self, request, book_id):
        ID = {"id": book_id}
        return render(request, "User/chapter_add.html", ID)

    def post(self, request, book_id):
        chap_name = request.POST.get('name')
        content = request.POST.get('content')
        if content != '':
            chap = chapter(chapter_name=chap_name, chapter_content=content, book_id=book_id)
            chap.save()
            return HttpResponseRedirect(reverse('book_detail', args=[book_id]))
        else:
            return HttpResponseRedirect(reverse('add_chap', args=[book_id]))

class update_chap(View):
    def get(self, request, book_id, chap_id):
        chap = chapter.objects.get(pk=chap_id)
        uchap = {"id": book_id, "chap": chap}
        return render(request, "User/chapter_update.html", uchap)

    def post(self, request, book_id, chap_id):
        chap_name = request.POST.get('name')
        content = request.POST.get('content')
        if content != '':
            chap = chapter.objects.get(pk=chap_id)
            chap.chapter_name = chap_name
            chap.chapter_content = content
            chap.save()
            return HttpResponseRedirect(reverse('book_detail', args=[book_id]))
        else:
            return HttpResponseRedirect(reverse('update_chap', args=[book_id,chap_id]))


class add_book(View):
    def get(self,request,user_id):
        ca = category.objects.all()
        to = topic.objects.all()
        add = {"id":user_id,"ca":ca,"to":to}
        return render(request,'User/book_add.html',add)
    def post(self,request,user_id):
        book_name = request.POST.get('book_name')
        if request.POST.get('tomtat') == '' or request.POST.get('tomtat') == ' ':
            tom_tat = 'Không có tóm tắt'
        else:
            tom_tat = request.POST.get('tomtat')

        if request.FILES['image']:
            image = request.FILES['image']
            fs = FileSystemStorage(location=logoRoot, base_url=logo_url)
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)

        insert_book = book(book_name=book_name, user_id=user_id, book_image=uploaded_file_url,book_synopsis=tom_tat)
        # try:
        insert_book.save()
        new_book = book.objects.all().filter(user_id=user_id, book_name=book_name).order_by('id').last()
        print('new_book', new_book)
        topics = request.POST.getlist('topics')
        categories = request.POST.getlist('categories')
        chapter_name = request.POST.get('chapter_name')
        content = request.POST.get('content')

        for item in topics:
            if item != "Null":
                cd_ds = topic_book(topic_id=item, book_id=new_book.id)
                try:
                    print('cd_ds', cd_ds)
                    cd_ds.save()
                except:
                    print("save topics_book that bai")
                    return HttpResponseRedirect(reverse('add_book', args=[user_id]))

        for item in categories:
            if item != "Null":
                tl_ds = category_book(category_id=item, book_id=new_book.id)
                try:
                    print('tl_ds', tl_ds)
                    tl_ds.save()
                except:
                    print("save categories_book that bai")
                    return HttpResponseRedirect(reverse('add_book', args=[user_id]))

        new_chapter = chapter(chapter_name=chapter_name, chapter_content=content, book_id=new_book.id)
        try:
            print('new_chapter', new_chapter)
            new_chapter.save()
        except:
            print("save chapter that bai")
            return HttpResponseRedirect(reverse('add_book', args=[user_id]))

        if request.POST.get('t_other') != '':
            t_other = request.POST.get('t_other').split(';')
            for item in t_other:
                if not topic.objects.filter(topic_name=item).exists():
                    add_topic = topic(topic_name=item)
                    try:
                        add_topic.save()
                    except:
                        print("save other_topic_book that bai")
                        return HttpResponseRedirect(reverse('add_book', args=[user_id]))
                print("item_topic", item)
                get_topic = topic.objects.get(topic_name=item)
                print("get_topic",get_topic)
                cd_ds = topic_book(topic_id=get_topic.id, book_id=new_book.id)
                try:
                    cd_ds.save()
                except:
                    return HttpResponseRedirect(reverse('add_book', args=[user_id]))

        if request.POST.get('c_other') != '':
            c_other = request.POST.get('c_other').split(';')
            for item in c_other:
                if not category.objects.filter(category_name=item).exists():
                    add_category = category(category_name=item)
                    try:
                        add_category.save()
                    except:
                        print("save other_category_book that bai")
                        return HttpResponseRedirect(reverse('add_book', args=[user_id]))
                print("item_category", item)
                get_category = category.objects.get(category_name=item)
                print("get_category", get_category)
                tl_ds = category_book(category_id=get_category.id, book_id=new_book.id)
                try:
                    tl_ds.save()
                except:
                    return HttpResponseRedirect(reverse('add_book', args=[user_id]))
        # except:
        #     print("save book that bai")
        #     return HttpResponseRedirect(reverse('add_book', args=[user_id]))

        return HttpResponseRedirect(reverse('book_list_manage', args=[user_id]))



class update_book(View):
    def get(self, request, book_id, user_id):
        ubook = book.objects.get(pk=book_id)
        ca = category.objects.all()
        to = topic.objects.all()
        b_ca = category_book.objects.all().filter(book_id=book_id)
        b_to = topic_book.objects.all().filter(book_id=book_id)

        update = {"id":user_id,"ubook":ubook,"ca":ca,"to":to,"b_ca":b_ca,"b_to":b_to}
        return render(request,'User/book_update.html',update)

    def post(self,request, book_id, user_id):
        ubook = book.objects.get(pk=book_id)

        book_name = request.POST.get('book_name')
        if request.POST.get('tomtat') == '' or request.POST.get('tomtat') == ' ':
            tom_tat = 'Không có tóm tắt'
        else:
            tom_tat = request.POST.get('tomtat')

        ubook.book_name = book_name
        update_book.book_synopsis = tom_tat

        if request.POST.get('image') != "":
            if request.FILES['image']:
                image = request.FILES['image']
                fs = FileSystemStorage(location=logoRoot, base_url=logo_url)
                filename = fs.save(image.name, image)
                uploaded_file_url = fs.url(filename)
                ubook.book_image = uploaded_file_url

        ubook.save()

        topics = request.POST.getlist('topics')
        delete_b_to = topic_book.objects.all().filter(book_id=book_id)
        delete_b_to.delete()
        for item in topics:
            cd_ds = topic_book(topic_id=item, book_id=book_id)
            try:
                print('cd_ds', cd_ds)
                cd_ds.save()
            except:
                print("save topics_book that bai")
                return HttpResponseRedirect(reverse('update_book', args=[book_id,user_id]))

        categories = request.POST.getlist('categories')
        delete_b_ca = category_book.objects.all().filter(book_id=book_id)
        delete_b_ca.delete()
        for item in categories:
            tl_ds = category_book(category_id=item, book_id=book_id)
            try:
                print('tl_ds', tl_ds)
                tl_ds.save()
            except:
                print("save categories_book that bai")
                return HttpResponseRedirect(reverse('update_book', args=[book_id,user_id]))

        #Other Topic
        if request.POST.get('t_other') != '':
            t_other = request.POST.get('t_other').split(';')
            for item in t_other:
                if not topic.objects.filter(topic_name=item).exists():
                    add_topic = topic(topic_name=item)
                    try:
                        add_topic.save()
                    except:
                        return HttpResponseRedirect(reverse('update_book', args=[book_id,user_id]))

                print("item_topic", item)
                get_topic = topic.objects.get(topic_name=item)
                print("get_topic",get_topic)
                cd_ds = topic_book(topic_id=get_topic.id, book_id=book_id)
                try:
                    cd_ds.save()
                except:
                    return HttpResponseRedirect(reverse('update_book', args=[book_id,user_id]))

        if request.POST.get('c_other') != '':
            c_other = request.POST.get('c_other').split(';')
            for item in c_other:
                if not category.objects.filter(category_name=item).exists():
                    add_category = category(category_name=item)
                    try:
                        add_category.save()
                    except:
                        print("save other_category_book that bai")
                        return HttpResponseRedirect(reverse('update_book', args=[book_id,user_id]))
                print("item_category", item)
                get_category = category.objects.get(category_name=item)
                print("get_category", get_category)
                tl_ds = category_book(category_id=get_category.id, book_id=book_id)
                try:
                    tl_ds.save()
                except:
                    return HttpResponseRedirect(reverse('update_book', args=[book_id,user_id]))
        return HttpResponseRedirect(reverse('book_list_manage', args=[user_id]))