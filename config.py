import os
class Config:
    '''
    General configuration parent class
    '''
    QUOTE_API_BASE_URL = "http://quotes.stormconsultancy.co.uk/random.json"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://clemence:34003@localhost/blogs'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")



class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass
    


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://clemence:34003@localhost/blogs'

    DEBUG = True
    
config_options = {
'development':DevConfig,
'production':ProdConfig
}

                                                                                                                                                                                                                                                                                                                                                                                                                                                      