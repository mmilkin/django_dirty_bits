from django.db import models
from dirty_bits import register


class Author(models.Model):
    name = models.TextField()


class Publisher(models.Model):
    name = models.TextField(null=True)


class Article(models.Model):
    """Good Authors get it right the first time"""
    author = models.OneToOneField(Author, primary_key=True)
    name = models.TextField(null=True, blank=True)


class NoteBook(models.Model):
    articles = models.ManyToManyField(Article, related_name='books', through='Volume')
    name = models.TextField(null=True, blank=True)


class Note(models.Model):
    content = models.TextField(null=True, blank=True)
    pages = models.IntegerField(null=True, default=2)
    article = models.ForeignKey(Article, related_name='notes', null=True, blank=True)

    def __unicode__(self):
        return self.content


class Person(models.Model):
    name = models.CharField(max_length=128)


class Volume(models.Model):
    article = models.ForeignKey(Article)
    book = models.ForeignKey(NoteBook)
    name = models.TextField(null=True, blank=True)


register(Note)
register(NoteBook)
register(Article)
register(Volume)

register(Person, strict=True)
