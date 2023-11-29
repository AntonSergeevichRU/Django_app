from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя автора', db_index=True)
    bio = models.TextField(null=False, blank=True, verbose_name='Биография автора')


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название категории', db_index=True)


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название тэга', db_index=True)



class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок статьи')
    content = models.TextField(null=True, verbose_name='Содержимое статьи')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации статьи')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Aвтор статьи')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория статьи')
    tags = models.ManyToManyField(Tag, verbose_name='Тэги статьи')

