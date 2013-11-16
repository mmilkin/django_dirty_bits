from django.test import TestCase
from dirty_test_bits.models import Article, Author, Note, NoteBook


class TestModels(TestCase):
    def setUp(self):
        super(TestModels, self).setUp()
        self.author = Author.objects.create(name='Steve')
        self.note_book = NoteBook.objects.create(name='Steve')
        self.article = Article.objects.create(author=self.author, name='Best article ever!')
        self.note = Note.objects.create(content='Best note ever!', article=self.article)

    def test_is_dirty_simple(self):
        self.assertTrue(self.note.is_dirty())
        note = Note.objects.get(pk=self.note.pk)
        self.assertFalse(note.is_dirty())
        note.content = 'Steve'
        self.assertTrue(note.is_dirty())

    def test_is_dirity_pages(self):
        note = Note.objects.get(pk=self.note.pk)
        note.pages = 7
        self.assertTrue(note.is_dirty())

    def test_is_dirty_fk(self):
        author = Author.objects.create(name='Bob')
        article = Article.objects.create(author=author, name='Almost the best article ever!')
        note = Note.objects.get(pk=self.note.pk)
        note.article = article
        self.assertTrue(note.is_dirty())
        note.save()

    def test_is_dirty_m2m(self):
        self.assertTrue(self.note_book.is_dirty())
        note_book = NoteBook.objects.get(pk=self.article.pk)
        self.assertFalse(note_book.is_dirty())
        author = Author.objects.create(name='Bob')
        article = Article.objects.create(author=author, name='Almost the best article ever!')
        note_book.articles.add(article)
        self.assertTrue(note_book.is_dirty())

    def test_is_dirty_1to1(self):
        author = Author.objects.create(name='Bob')
        self.article.author = author
        self.assertTrue(self.article.is_dirty())

    def test_unregistered(self):
        self.assertFalse(hasattr(self.author, 'is_dirty'))
