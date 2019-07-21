import logging
import os


from django import template
from django.conf import settings

from git import Repo, InvalidGitRepositoryError

log = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def version(max_length=8):
    revision = 'EOS'

    try:
        root = str(settings.PROJECT_ROOT)  # normalize environ.Path to str if django-environ is used

        try:
            repo = Repo(root)
            if not repo.bare:
                revision = repo.commit('HEAD').hexsha
        except InvalidGitRepositoryError:
            pass

        revision_file = os.path.join(root, '.gitcommit')
        if os.path.isfile(os.path.join(root, revision_file)):
            with open(revision_file) as f:
                revision = f.read().strip()
    except Exception as e:
        log.error('Could not resolve revision in version template tag: {}'.format(e), exc_info=True)

    return revision[:max_length]
