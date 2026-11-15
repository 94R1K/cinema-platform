
class ContentDatabaseRouter:
    content_app_label = 'movies'
    content_database = 'content'

    def db_for_read(self, model, **_hints):
        if model._meta.app_label == self.content_app_label:
            return self.content_database

        return None

    def db_for_write(self, model, **_hints):
        if model._meta.app_label == self.content_app_label:
            return self.content_database

        return None

    def allow_relation(self, obj1, obj2, **_hints):
        obj1_is_content = (
            obj1._meta.app_label == self.content_app_label
        )
        obj2_is_content = (
            obj2._meta.app_label == self.content_app_label
        )

        if obj1_is_content and obj2_is_content:
            return True

        if obj1_is_content or obj2_is_content:
            return False

        return None

    def allow_migrate(
        self,
        db,
        app_label,
        _model_name=None,
        **_hints,
    ):
        if app_label == self.content_app_label:
            return False

        return db == 'default'
