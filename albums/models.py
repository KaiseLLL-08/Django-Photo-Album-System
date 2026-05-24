from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    """
    An Album is a collection of photos.
    Each Album belongs to one User (the owner).
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # If user is deleted, delete their albums too
        related_name='albums'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return self.title


class Photo(models.Model):
    """
    A Photo belongs to one Album.
    Images are stored on Cloudinary, not locally.
    """
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,  # If album deleted, delete its photos
        related_name='photos'
    )
    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/')  # Goes to Cloudinary
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title