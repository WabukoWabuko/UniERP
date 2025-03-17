class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.app_label == 'authentication':
            return 'default'
        return model._meta.app_label

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.app_label == 'authentication':
            return 'default'
        return model._meta.app_label

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations between default (auth) and ERP apps
        if obj1._meta.app_label == 'auth' and obj2._meta.app_label in ['education_erp', 'small_business_erp']:
            return True
        if obj2._meta.app_label == 'auth' and obj1._meta.app_label in ['education_erp', 'small_business_erp']:
            return True
        # Same app, allow
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'auth' or app_label == 'authentication':
            return db == 'default'
        return db == app_label
