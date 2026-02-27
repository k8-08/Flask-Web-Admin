# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'flask-secret-key-change-in-prod')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-prod')
    JWT_EXPIRE_HOURS = int(os.getenv('JWT_EXPIRE_HOURS', 24))
    
    # Database - 同步 MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'MYSQL_DATABASE_URI_SYNC',
        'mysql+pymysql://root:123456@localhost:3306/fastapiwebadmin'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # CORS
    CORS_ORIGINS = ['*']


config = Config()
