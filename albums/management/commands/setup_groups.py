from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from albums.models import Album, Photo


class Command(BaseCommand):
    help = 'Create default user groups and permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        admin_group, _ = Group.objects.get_or_create(name='Administrator')
        user_group, _ = Group.objects.get_or_create(name='Standard User')

        # Get content types
        album_ct = ContentType.objects.get_for_model(Album)
        photo_ct = ContentType.objects.get_for_model(Photo)

        # Get permissions
        album_perms = Permission.objects.filter(content_type=album_ct)
        photo_perms = Permission.objects.filter(content_type=photo_ct)

        # Administrator gets ALL permissions
        admin_group.permissions.set(list(album_perms) + list(photo_perms))

        # Standard User gets limited permissions
        user_perms = Permission.objects.filter(
            content_type__in=[album_ct, photo_ct],
            codename__in=['view_album', 'add_photo', 'change_photo', 'view_photo']
        )
        user_group.permissions.set(user_perms)

        self.stdout.write(self.style.SUCCESS('Groups created successfully!'))