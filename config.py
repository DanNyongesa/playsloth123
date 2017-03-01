import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4ODIwNTc2MiwiaWF0IjoxNDg4MTY5NzYy'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    PLAY_ADMIN = os.environ.get('ADMIN') or ''
    PLAY_MAIL_SENDER = '254Playsinc Admin 254plays@gmail.com'
    MAIL_SUBJECT_PREFIX = '[254plays]'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'wav', 'mp3', 'mp4'])

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "play@gmail.com"
    MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD')  or "password"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADED_IMAGES_DEST') or os.path.join(basedir, 'app/media')
    UPLOADS_DEFAULT_URL = os.environ.get('UPLOADED_IMAGES_URL') or 'http://localhost:5000/app/media/'
    # UPLOADED_MEDIA_DEST = os.environ.get('UPLOADED_MEDIA_DEST') or basedir
    # UPLOADED_MEDIA_URL = os.environ.get('UPLOADED_MEDIA_URL') or 'http://localhost:5000/'


class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}