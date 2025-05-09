# Generated by Django 5.2 on 2025-04-20 14:01

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('subtitle', models.CharField(blank=True, max_length=500)),
                ('authors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=None)),
                ('isbn', models.CharField(blank=True, max_length=20, unique=True)),
                ('publisher', models.CharField(blank=True, max_length=200)),
                ('published_date', models.DateField(blank=True, null=True)),
                ('edition', models.CharField(blank=True, max_length=50)),
                ('page_count', models.PositiveIntegerField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=50)),
                ('genres', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('subjects', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), default=list, size=None)),
                ('keywords', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('mood_tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=list, size=None)),
                ('age_range', models.CharField(blank=True, max_length=20)),
                ('author_countries', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None)),
                ('setting_country', models.CharField(blank=True, max_length=100)),
                ('cover_image', models.URLField(blank=True)),
                ('purchase_links', models.JSONField(default=dict)),
                ('borrow_links', models.JSONField(default=dict)),
                ('average_rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
            ],
            options={
                'ordering': ['title'],
                'indexes': [models.Index(fields=['title'], name='books_book_title_d3218d_idx'), models.Index(fields=['authors'], name='books_book_authors_ff5846_idx'), models.Index(fields=['genres'], name='books_book_genres_7343b7_idx'), models.Index(fields=['setting_country'], name='books_book_setting_530ebf_idx')],
            },
        ),
    ]
