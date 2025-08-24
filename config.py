import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'correct-horse-battery-staple'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 280}
    
    # S3_ENDPOINT = os.environ.get('R2_ENDPOINT')
    # S3_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
    # S3_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
    # S3_BUCKET_NAME = 's3bucket'
    # S3_REGION = 'eeur'

    # CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    # CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    # CLOUDINARY_NAME = os.environ.get('CLOUDINARY_NAME')

    LOG_TO_STDOUT = int(os.environ.get('LOG_TO_STDOUT') or 1)
    
    MAX_CONTENT_LENGTH = 20 * 1000 * 1000
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.jp2', '.j2k']
    THUMB_SIZE = (300,300)

    LANGUAGES = ['en', 'et']

    SESSION_COOKIE_SAMESITE = "strict"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "strict"
    REMEMBER_COOKIE_SECURE = True
