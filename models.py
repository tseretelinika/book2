from sqlalchemy import ForeignKey
from ext import db, login_manager
from flask_login import UserMixin

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String(), default="Guest")


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

class Book(db.Model, BaseModel):
    __tablename__ = "books"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)



class Review(db.Model, BaseModel):
    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    book_id = db.Column(ForeignKey("books.id"))
