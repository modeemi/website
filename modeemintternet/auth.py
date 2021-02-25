from secrets import token_hex

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.timezone import now

from passlib.hash import des_crypt, md5_crypt, sha256_crypt, sha512_crypt

from modeemintternet.models import Format, Passwd, Shadow, ShadowFormat


@transaction.atomic
def update_password(username, new_password) -> None:
    """
    Generate new password hashes to database for modern supported values.
    """

    # Use same fixed timestamp for updates in both shadow and shadow format tables
    last_updated = now()

    # Generate new hashes for all values
    new_hashes = {
        "SHA512": sha512_crypt.hash(new_password),
        "SHA256": sha256_crypt.hash(new_password),
        "MD5": md5_crypt.hash(new_password),
        "DES": "*LK*",  # locked
    }

    passwd = Passwd.objects.get(username=username)
    shadow = Shadow.objects.get(username=passwd)
    shadow.lastchanged = int(last_updated.timestamp()) // 86400
    shadow.save()

    # Delete all old hashes from the database
    # since this view is run inside a single atomic transaction
    # there is no risk of leaving the database to a defunct state
    ShadowFormat.objects.filter(username=passwd).delete()

    for existing_format in Format.objects.all():
        # These are the currently updated hasher values
        # database formats table can have extra values but they are not processed
        new_hash = new_hashes.get(existing_format.format, None)

        # Write new hashes for supported formats
        if new_hash:
            ShadowFormat.objects.create(
                username=passwd,
                format=existing_format,
                hash=new_hash,
                last_updated=last_updated,
            )


@transaction.atomic
def check_password(username, password) -> bool:
    """
    Compare password against existing external user database.

    Note that this method only compares the password with the first found comparison hash.
    """

    hashers = {
        "SHA512": sha512_crypt,
        "SHA256": sha256_crypt,
        "MD5": md5_crypt,
        # "DES": should always be unusable i.e. "*LK*" so no reason to have it included in checkers
        # Support authentication from old imported legacy hash values.
        "OLD_SHA512": sha512_crypt,
        "OLD_SHA256": sha256_crypt,
        "OLD_MD5": md5_crypt,
        "OLD_DES": des_crypt,  # only for legacy hash checking, not generation.
    }

    # Values that can not be processed by passlib hasher but are valid in *nix passwd.
    # https://en.wikipedia.org/wiki/Passwd
    skipped_hash_values = {
        "",  # no entry
        "!",  # password locked
        "*",  # password locked
        "*LK*",  # account locked
        "*NP*",  # password not set
        "!!",  # password not set
    }

    # Get valid and comparable hash values from database in one roundrip.
    shadow_format_hashes = {
        shadow_format.format.format: shadow_format.hash
        for shadow_format in ShadowFormat.objects.only("format__format", "hash")
        .select_related("format")
        .exclude(hash__in=skipped_hash_values)
        .filter(username=username)
    }

    # Find the first usable hash - hasher combination and check it for validity.
    for hash_format, hasher in hashers.items():
        existing_hash = shadow_format_hashes.get(hash_format)
        if existing_hash:
            return hasher.verify(password, existing_hash)

    # No hash was found so we run a hasher once to reduce the timing delta between
    # existing and non-existing users to mitigate enumeration attacks.
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
            # This detail stems from the stock Django model backend.
            UserModel().set_password(password)
        else:
            if check_password(username, password) and self.user_can_authenticate(user):
                return user
