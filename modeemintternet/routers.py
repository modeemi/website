from . import models


class Router:
    @staticmethod
    def db_for_read(model, **hints):
        if model in (models.Passwd, models.Shadow, models.UserGroup):
            return 'modeemiuserdb'
        return None

    @staticmethod
    def db_for_write(model, **hints):
        if model in (models.Passwd, models.Shadow, models.UserGroup):
            return 'modeemiuserdb'
        return None
