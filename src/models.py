from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[list['Favorite']] = relationship('Favorite', back_populates = 'user')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Character(db.Model):
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "hair_color" : self.hair_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
        }
    
class Planet(db.Model):
    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    diameter: Mapped[float] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    gravity: Mapped[float] = mapped_column(nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "diameter" : self.diameter,
            "population": self.population,
            "gravity": self.gravity,

        }

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates = 'favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id" : self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,

        }