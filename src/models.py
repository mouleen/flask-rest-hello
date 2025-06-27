from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey,CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(140), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(140), nullable=False)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites": [fav.serialize() for fav in self.favorites]
        }

class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="people")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": "/people/"+str(self.id)
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": "/planet/"+str(self.id)
        }

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="vehicle")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": "/vehicle/"+str(self.id)
        }

class Favorite(db.Model):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[Optional[int]] = mapped_column(ForeignKey("people.id"), nullable=True)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vehicle.id"), nullable=True)
    
    __table_args__ = (
        CheckConstraint(
            "(people_id IS NOT NULL)::int + "
            "(planet_id IS NOT NULL)::int + "
            "(vehicle_id IS NOT NULL)::int = 1",
            name="check_only_one_fk_not_null"
        ),
    )
    user: Mapped["User"] = relationship(back_populates="favorites")
    people: Mapped[Optional["People"]] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planet"]] = relationship(back_populates="favorites")
    vehicle: Mapped[Optional["Vehicle"]] = relationship(back_populates="favorites")

    def serialize(self):
        return {
             "id": self.id,
            "user_id": self.user_id,
            "favorite_type": self.get_type(),
            "favorite_data": self.get_data()
        }

    def get_type(self) -> str:
        if self.people_id is not None:
            return "people"
        elif self.planet_id is not None:
            return "planet"
        elif self.vehicle_id is not None:
            return "vehicle"
        return "unknown"

    def get_data(self) -> Optional[dict]:
        if self.people:
            return self.people.serialize()
        if self.planet:
            return self.planet.serialize()
        if self.vehicle:
            return self.vehicle.serialize()
        return None

    def get_element_id(self) -> Optional[int]:
        if self.people_id is not None:
            return self.people_id
        elif self.planet_id is not None:
            return self.planet_id
        elif self.vehicle_id is not None:
            return self.vehicle_id
        return None
    

