from flask_login import UserMixin
from extensions import db
from sqlalchemy.orm import relationship
from flask import request


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey("brand_name.brandname"))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    brand_name = db.Column(db.String(100))
    profile_link = db.Column(db.String(250), unique=True)
    # brand = relationship("ChooseBrandName", back_populates="brand") #THIS IS NOT IN USE
    posts = relationship("CreateProfile", back_populates="author")


def get_profile_link(brand_name):
    return f"{request.host_url}{brand_name}"
