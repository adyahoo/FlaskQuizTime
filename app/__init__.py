from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class BaseDB(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=BaseDB)

app = Flask(__name__)
app.secret_key = 'kodland_pro_python_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

from app import routes
