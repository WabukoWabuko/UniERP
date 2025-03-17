class DatabaseRouter:
    ERP_APPS = ['education_erp', 'small_business_erp']  # Add other 8 later

    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.ERP_APPS:
            return app_label
        return 'default'  # Built-in apps (auth, sessions, etc.) go to default

    def db_for_write(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.ERP_APPS:
            return app_label
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        app1, app2 = obj1._meta.app_label, obj2._meta.app_label
        # Allow relations between default (auth) and ERP apps
        if app1 == 'auth' and app2 in self.ERP_APPS:
            return True
        if app2 == 'auth' and app1 in self.ERP_APPS:
            return True
        # Same app, allow
        if app1 == app2:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.ERP_APPS:
            return db == app_label
        return db == 'default'  # Built-in apps migrate to default
