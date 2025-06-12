from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(60), unique=False, nullable=True)
    lastname: Mapped[str] = mapped_column(String(60), unique=False, nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(60), unique=False, nullable=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))


    def serialize(self):
        return {
            "id": self.id,
            "autor": self.autor, #completar
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))



    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.autor, #completar
            # do not serialize the password, its a security breach
        }


class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[int] = mapped_column(unique=False, nullable=False) 
    url: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))


    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url, #completar
            "post": self.url, #representar el Post completo
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
    __tablename__ = "follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

