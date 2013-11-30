from mock import patch, call

from django.test import TestCase
from dirty_bits import register_all
from dirty_test_bits.models import (
    Article,
    Author,
    Note,
    NoteBook,
    Person,
    Volume,
)


class TestDirtySignals(TestCase):
    def setUp(self):
        super(TestDirtySignals, self).setUp()
        self.author = Author.objects.create(name='Steve')
        self.note_book = NoteBook.objects.create(name='Steve')
        self.article = Article.objects.create(author=self.author, name='Best article ever!')
        self.volume = Volume.objects.create(
            book=self.note_book,
            article=self.article,
            name='Book 1'
        )
        self.note = Note.objects.create(content='Best note ever!', article=self.article)

    def test_is_dirty_simple(self):
        note = Note(content='Best note ever!')
        self.assertTrue(note.is_dirty())
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
        notebook = NoteBook(name='Steve')
        self.assertTrue(notebook.is_dirty())
        note_book = NoteBook.objects.get(pk=self.article.pk)
        self.assertFalse(note_book.is_dirty())
        author = Author.objects.create(name='Bob Smith')
        article = Article.objects.create(author=author, name='Almost the best article ever 2!')
        Volume.objects.create(
            book=note_book,
            article=article,
            name='Book 2'
        )
        # we are not tracking many to many relationships since they
        # are django saved on add any way
        self.assertFalse(note_book.is_dirty())

    def test_is_dirty_1to1(self):
        author = Author.objects.create(name='Bob')
        self.article.author = author
        self.assertTrue(self.article.is_dirty())

    def test_unregistered(self):
        self.assertFalse(hasattr(self.author, 'is_dirty'))

    @patch('dirty_bits.register')
    def test_register_all(self, register):
        register_all()
        calls = register.call_args_list
        self.assertTrue(call(Note, False) in calls)
        self.assertTrue(call(NoteBook, False) in calls)
        self.assertTrue(call(Author, False) in calls)
        self.assertTrue(call(Article, False) in calls)

    @patch('dirty_bits.register')
    def test_register_all_strict(self, register):
        register_all(strict=True)
        calls = register.call_args_list
        self.assertTrue(call(Note, True) in calls)
        self.assertTrue(call(NoteBook, True) in calls)
        self.assertTrue(call(Author, True) in calls)
        self.assertTrue(call(Article, True) in calls)

    def test_post_save_dirty(self):
        notebook = NoteBook(name='Steve')
        self.assertTrue(notebook.is_dirty())
        notebook.save()
        self.assertFalse(notebook.is_dirty())


class StrongCheckingTestCase(TestCase):

    def setUp(self):
        super(StrongCheckingTestCase, self).setUp()
        self.author = Author.objects.create(name='Sr Steve')
        self.article = Article.objects.create(
            author=self.author,
            name='Best article ever!'
        )
        self.person = Person.objects.create(name='Steve')


    @patch('dirty_bits.hash_fnc')
    def test_checking_dirty_strict(self, hash_fnc):
        hash_fnc.return_value = 23
        self.person = Person.objects.get(pk=self.person.pk)
        self.person.name = 'Bob'
        self.assertTrue(self.person.is_dirty())

    @patch('dirty_bits.hash_fnc')
    def test_checking_dirty_non_strict(self, hash_fnc):
        hash_fnc.return_value = 23
        article = Article.objects.get(pk=self.article.pk)
        article.name = 'Bobs best article'
        self.assertFalse(article.is_dirty())
