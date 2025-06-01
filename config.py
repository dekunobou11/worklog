# config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
    UPLOAD_FOLDER = "uploads"
    EXPORT_FOLDER = "export"
    DATABASE = "memoapp.sqlite"
    KEY_FILE = "secret.key"

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
