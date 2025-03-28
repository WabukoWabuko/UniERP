class DatabaseRouter:
    ERP_APPS = ['education_erp', 'small_business_erp']
    BUILTIN_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'rest_framework_simplejwt',
        'corsheaders',
        'allauth',
        'allauth.account',
    ]

    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.ERP_APPS:
            return app_label
        return 'default'  # Built-ins go to default

    def db_for_write(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.ERP_APPS:
            return app_label
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        app1, app2 = obj1._meta.app_label, obj2._meta.app_label
        # Allow relations between contenttypes and ERP apps
        if 'django.contrib.contenttypes' in (app1, app2) and (app1 in self.ERP_APPS or app2 in self.ERP_APPS):
            return True
        # Only allow relations within the same app otherwise
        return app1 == app2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.ERP_APPS:
            return db == app_label
        return db == 'default'  # Built-ins migrate to default
