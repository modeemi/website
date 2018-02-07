from . import models

MODEEMIUSERDB_MODELS = (
    models.Format,
    models.Passwd,
    models.Shadow,
    models.ShadowFormat,
    models.UserGroup,
    models.UserGroupMember
)


class Router:
    @staticmethod
    def db_for_read(model, **hints):
        if model in MODEEMIUSERDB_MODELS:
            return 'modeemiuserdb'
        return None

    @staticmethod
    def db_for_write(model, **hints):
        if model in MODEEMIUSERDB_MODELS:
            return 'modeemiuserdb'
        return None
