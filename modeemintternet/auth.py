from secrets import token_hex

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from passlib.hash import des_crypt, md5_crypt, sha256_crypt, sha512_crypt

from modeemintternet.models import ShadowFormat


def check_password(username, password) -> bool:
    """
    Compare password against existing external user database.

    Note that this method only compares the password with the first found comparison hash.
    """

    hashers = {
        "SHA512": sha512_crypt,
        "SHA256": sha256_crypt,
        "MD5": md5_crypt,
        # "DES": should always be locked i.e. "*LK*" nowadays
        # Support authentication from old imported legacy hash values
        "OLD_SHA512": sha512_crypt,
        "OLD_SHA256": sha256_crypt,
        "OLD_MD5": md5_crypt,
        "OLD_DES": des_crypt,
    }

    # Values that can not be processed by passlib hasher but are valid in *nix passwd
    # https://en.wikipedia.org/wiki/Passwd
    skip = [
        "",  # no entry
        "!",  # password locked
        "*",  # password locked
        "*LK*",  # account locked
        "*NP*",  # password not set
        "!!",  # password not set
    ]

    shadow_format_hashes = ShadowFormat.objects.filter(username=username)
    for name, hasher in hashers.items():
        try:
            shadow_format_hash = shadow_format_hashes.get(format=name).hash
            if shadow_format_hash not in skip:
                return hasher.verify(password, shadow_format_hash)
        except ShadowFormat.DoesNotExist:
            continue

    # Run a hasher once to reduce the timing difference between
    # existing and non-existing users and to mitigate enumeration attacks
    sha512_crypt.hash(token_hex(42))

    return False


class ModeemiUserDBBackend(ModelBackend):
    def authenticate(  # pylint: disable=inconsistent-return-statements
        self, request, username=None, password=None, **kwargs
    ):
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel._default_manager.get_by_natural_key(  # pylint: disable=protected-access
                username
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if check_password(username, password) and self.user_can_authenticate(user):
                return user
