from django.db import models
import uuid #Required for unique book instances. Generates universally unique identifiers
from django.urls import reverse # Used to generate URLS by reversing the URL pattern
import uuid 
# Create your models here.

class Genre(models.Model):
	'''Model representing a book genre.'''
	name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

	def __str__(self):
		"""String for representing the Model object."""
		return self.name

class Book(models.Model):
	# Title of the book. CharField represents a short string. Maximum length is set at 200 characters.
	title = models.CharField(max_length=200)
	# Author of the book. A foreignKey is used when the field Author can point to many books, but a book can only have one author. 
	# The on_delete is SET_NULL so that Django knows what to do with the instance if deleted, and null=True is so if deleted, the field would be replaced by null
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	# Summary of the book. Textfield is for longer strings. 
	summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book...or else!")
	# ISBN of the book. unique=True sets so that only one isbn can be set for a given book. 
	isbn = models.CharField('ISBN',max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
	# Genre class, which is defined above.
	genre = models.ManytoManyField(Genre, help_text='Select a genre for this book')

	def __str__(self):
		return self.title

	def get_absolute_url(self): 
		"""Returns the URL to access a detail record for this book."""
		return reverse('book-detail', args=[str(self.id)]

class BookInstance(models.Model):

	# The UUIDField is a python module used to universally unique identifiers to act as an id for each book instance 
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
	help_text='Unique ID for this particular book across whole library')
	
	book = models.ForeignKey('Book',on_delete=Models.RESTRICT, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)

	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	)
 
	status = models.CharField(
		max_length=1,
		choices=LOAN_STATUS,
		blank=True,
		default='m',
		help_text='Book availability',
	)
	class Meta:
		ordering = ['due_back']

	def __str__(self):
		"""String for representing the Model object."""
		return f'{self.id} ({self.book.title})'
