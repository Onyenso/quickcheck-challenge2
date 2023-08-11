from .base import *
import dj_database_url

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default="postgres://alphadev:0SM9vX5QU5xRc4Zhp4h4AWTdAPVj6bBd@dpg-cjaqiapitvpc73bj6hvg-a.oregon-postgres.render.com/quickcheck",
        conn_max_age=600
    )
}
