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
        if app_label == 'auth' and model._meta.model_name == 'user':
            return 'education_erp'  # AUTH_USER_MODEL goes to education_erp
        return 'default'  # Built-ins go to default

    def db_for_write(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in self.ERP_APPS:
            return app_label
        if app_label == 'auth' and model._meta.model_name == 'user':
            return 'education_erp'  # AUTH_USER_MODEL goes to education_erp
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        app1, app2 = obj1._meta.app_label, obj2._meta.app_label
        # Allow relations between contenttypes and ERP apps
        if 'django.contrib.contenttypes' in (app1, app2) and (app1 in self.ERP_APPS or app2 in self.ERP_APPS):
            return True
        # Allow relations between auth and contenttypes (e.g., Permission.content_type)
        if 'django.contrib.auth' in (app1, app2) and 'django.contrib.contenttypes' in (app1, app2):
            return True
        # Allow relations between auth.User and education_erp models
        if app1 == 'auth' and obj1._meta.model_name == 'user' and app2 == 'education_erp':
            return True
        if app2 == 'auth' and obj2._meta.model_name == 'user' and app1 == 'education_erp':
            return True
        # Only allow relations within the same app otherwise
        return app1 == app2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.ERP_APPS:
            return db == app_label
        if app_label == 'auth' and model_name == 'user':
            return db == 'education_erp'  # AUTH_USER_MODEL migrates to education_erp
        return db == 'default'  # Built-ins migrate to default
