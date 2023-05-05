from django.db import models
from User.models import customer_user
# from .permission import user_only_view_by_user_id_permissions

# Create your models here.
class book(models.Model):
    book_name = models.CharField(max_length=100, null=False)
    book_image = models.ImageField(upload_to='images/')
    book_synopsis = models.TextField(max_length=1000, default='Không có tóm tắt')
    status = models.IntegerField(default=1)
    user = models.ForeignKey(customer_user, on_delete=models.CASCADE)

    # class Meta:
    #     permissions = (
    #         ('user_view_book', 'Can view book'),
    #     )

    def __str__(self):
        return f"(book_id.{self.id}): {self.book_name}"


class topic(models.Model):
    topic_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.topic_name


class category(models.Model):
    category_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.category_name


class chapter(models.Model):
    chapter_name = models.CharField(max_length=100, default='')
    chapter_content = models.TextField(null=False)
    date_create = models.DateField(auto_now_add=True)
    view_number = models.IntegerField(default=0)
    book = models.ForeignKey(book, on_delete=models.CASCADE)

    def __str__(self):
        return f"(id.{self.book.id}) {self.chapter_name}"


class topic_book(models.Model):
    book = models.ForeignKey(book, on_delete=models.CASCADE)
    topic = models.ForeignKey(topic, on_delete=models.CASCADE)

    def __str__(self):
        return f"(topic_id.{self.topic.id}) {self.topic.topic_name} : (book_id.{self.book.id}) {self.book.book_name}"


class category_book(models.Model):
    book = models.ForeignKey(book, on_delete=models.CASCADE)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    def __str__(self):
        return f"(category_id.{self.category.id}) {self.category.category_name} : (book_id.{self.book.id}) {self.book.book_name}"

class rating(models.Model):
    book = models.ForeignKey(book, on_delete=models.CASCADE)
    user = models.ForeignKey(customer_user, on_delete=models.CASCADE)
    rating_type = models.IntegerField(default=0)


class comment(models.Model):
    chapter = models.ForeignKey(chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(customer_user, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    date_submit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.user.fullname}) {self.content}"
