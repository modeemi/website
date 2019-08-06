from passlib.hash import (
    md5_crypt,
    sha256_crypt,
    sha512_crypt,
)

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from .models import ShadowFormat


def check_password(username, password) -> bool:
    """
    Compare password against existing external user database.

    Note that this method only compares the password with the first found comparison hash.
    """

    hashers = {
        'SHA512': sha512_crypt,
        'SHA256': sha256_crypt,
        'MD5': md5_crypt,
    }

    shadow_formats = ShadowFormat.objects.filter(
        username=username,
        format__in=hashers.keys(),
    )

    for name, hasher in hashers.items():
        try:
            shadow_format_hash = shadow_formats.get(format=name).hash
            return hasher.verify(password, shadow_format_hash)
        except ShadowFormat.DoesNotExist:
            continue

    return False


class ModeemiUserDBBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if check_password(username, password) and self.user_can_authenticate(user):
                return user
