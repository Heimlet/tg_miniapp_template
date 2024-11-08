from django.contrib.auth.models import Permission


def get_user_permissions(user):
    if user.is_superuser:
        permissions_qs = Permission.objects.all()
    else:
        permissions_qs = user.user_permissions.all() | Permission.objects.filter(group__user=user)

    permissions_qs = permissions_qs.distinct().values('content_type__app_label', 'codename')

    formatted_permissions = [f"{perm['content_type__app_label']}.{perm['codename']}" for perm in permissions_qs]

    return sorted(set(formatted_permissions))
