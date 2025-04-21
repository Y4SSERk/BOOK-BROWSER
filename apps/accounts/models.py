from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

    def create_default_shelves(self):
        """Create default shelves for new users"""
        default_shelves = [
            ('SAVED', 'Saved Books'),
            ('BORROWED', 'Borrowed Books'),
            ('PURCHASED', 'Purchased Books'),
        ]
        
        for shelf_type, name in default_shelves:
            Shelf.objects.get_or_create(
                profile=self,
                shelf_type=shelf_type,
                defaults={'name': name}
            )

class Shelf(models.Model):
    SHELF_TYPES = [
        ('SAVED', 'Saved Books'),
        ('BORROWED', 'Borrowed Books'),
        ('PURCHASED', 'Purchased Books'),
        ('CUSTOM', 'Custom Shelf'),
    ]
    
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='shelves'
    )
    shelf_type = models.CharField(
        max_length=10,
        choices=SHELF_TYPES,
        default='CUSTOM'
    )
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(
        'books.Book',
        related_name='shelves',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'shelf_type'],
                name='unique_default_shelves',
                condition=models.Q(shelf_type__in=['SAVED', 'BORROWED', 'PURCHASED']),
            )
        ]
        ordering = ['created_at']
        verbose_name_plural = 'Shelves'

    def __str__(self):
        return f"{self.profile.user.username}'s {self.name}"
