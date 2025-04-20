from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Book(models.Model):
    # Core Identification
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True)
    authors = ArrayField(models.CharField(max_length=200), default=list)
    isbn = models.CharField(max_length=20, blank=True, unique=True)
    
    # Publication Info
    publisher = models.CharField(max_length=200, blank=True)
    published_date = models.DateField(null=True, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, blank=True)
    
    # Content Classification
    genres = ArrayField(models.CharField(max_length=100), default=list)
    subjects = ArrayField(models.CharField(max_length=200), default=list)
    keywords = ArrayField(models.CharField(max_length=100), default=list)
    mood_tags = ArrayField(models.CharField(max_length=50), default=list)
    age_range = models.CharField(max_length=20, blank=True)
    
    # Geographic Data
    author_countries = ArrayField(models.CharField(max_length=100), default=list)
    setting_country = models.CharField(max_length=100, blank=True)
    
    # Media & Links
    cover_image = models.URLField(blank=True)
    
    # Purchase/Access Options
    purchase_links = models.JSONField(default=dict)  # Changed to django.db.models.JSONField
    borrow_links = models.JSONField(default=dict)    # Changed to django.db.models.JSONField
    
    # Ratings
    average_rating = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['authors']),
            models.Index(fields=['genres']),
            models.Index(fields=['setting_country']),
        ]
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {', '.join(self.authors)}"