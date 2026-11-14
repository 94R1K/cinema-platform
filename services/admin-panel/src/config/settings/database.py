import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    },
    'content': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['CONTENT_POSTGRES_DB'],
        'USER': os.environ['CONTENT_POSTGRES_USER'],
        'PASSWORD': os.environ['CONTENT_POSTGRES_PASSWORD'],
        'HOST': os.environ['CONTENT_POSTGRES_HOST'],
        'PORT': os.getenv('CONTENT_POSTGRES_PORT', '5432'),
    },
}


DATABASE_ROUTERS = [
    'movies.db_router.ContentDatabaseRouter',
]
