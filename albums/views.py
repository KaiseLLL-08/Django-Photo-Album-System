from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm


# ─── Mixins (Reusable permission helpers) ────────────────────────────────────

class AdminRequiredMixin(UserPassesTestMixin):
    """Only Administrators can access this view."""
    def test_func(self):
        return self.request.user.groups.filter(name='Administrator').exists() \
               or self.request.user.is_superuser


class OwnerOrAdminMixin(UserPassesTestMixin):
    """Only the owner or an Administrator can access this view."""
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        is_admin = user.groups.filter(name='Administrator').exists() or user.is_superuser
        if hasattr(obj, 'owner'):
            return obj.owner == user or is_admin
        elif hasattr(obj, 'uploader'):
            return obj.uploader == user or is_admin
        return False


# ─── Home ─────────────────────────────────────────────────────────────────────

class HomeView(TemplateView):
    template_name = 'home.html'


# ─── Authentication ───────────────────────────────────────────────────────────

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Assign new users to Standard User group
        user = self.object
        group = Group.objects.get(name='Standard User')
        user.groups.add(group)
        messages.success(self.request, 'Account created! Please log in.')
        return response


# ─── Album Views ──────────────────────────────────────────────────────────────

class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'

    def get_queryset(self):
        user = self.request.user
        is_admin = user.groups.filter(name='Administrator').exists() or user.is_superuser
        if is_admin:
            return Album.objects.all()
        # Standard users see public albums AND their own
        return Album.objects.filter(owner=user) | Album.objects.filter(is_public=True)


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        context['is_owner'] = self.object.owner == self.request.user
        context['is_admin'] = (
            self.request.user.groups.filter(name='Administrator').exists()
            or self.request.user.is_superuser
        )
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'
    success_url = reverse_lazy('album-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the owner to the logged-in user
        messages.success(self.request, 'Album created successfully!')
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, OwnerOrAdminMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'albums/album_form.html'
    success_url = reverse_lazy('album-list')

    def form_valid(self, form):
        messages.success(self.request, 'Album updated successfully!')
        return super().form_valid(form)


class AlbumDeleteView(LoginRequiredMixin, OwnerOrAdminMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('album-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Album deleted.')
        return super().delete(request, *args, **kwargs)


# ─── Photo Views ──────────────────────────────────────────────────────────────

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        messages.success(self.request, 'Photo uploaded successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.album.pk})


class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'albums/photo_detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['can_edit'] = (
            self.object.uploader == user
            or user.groups.filter(name='Administrator').exists()
            or user.is_superuser
        )
        return context


class PhotoUpdateView(LoginRequiredMixin, OwnerOrAdminMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'albums/photo_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Photo updated!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.album.pk})


class PhotoDeleteView(LoginRequiredMixin, OwnerOrAdminMixin, DeleteView):
    model = Photo
    template_name = 'albums/photo_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.album.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Photo deleted.')
        return super().delete(request, *args, **kwargs)