from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, declarative_base, sessionmaker
from eralchemy2 import render_er

Base = declarative_base()

engine = create_engine('sqlite:///starwars.db')
Session = sessionmaker(bind=engine)
session = Session()

user_favorites_table = Table('user_favorites', Base.metadata,
                             Column('user_id', Integer, ForeignKey('users.id')),
                             Column('favorite_id', Integer, ForeignKey('favorites.id')))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    favorites = relationship("Favorite", 
                             secondary=user_favorites_table,
                             back_populates="users")


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'favorite',
        'polymorphic_on': type
    }

    users = relationship("User", 
                         secondary=user_favorites_table,
                         back_populates="favorites")


class Character(Favorite):
    __tablename__ = 'characters'
    id = Column(Integer, ForeignKey('favorites.id'), primary_key=True)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'character',
    }


class Planet(Favorite):
    __tablename__ = 'planets'
    id = Column(Integer, ForeignKey('favorites.id'), primary_key=True)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'planet',
    }


class Vehicle(Favorite):
    __tablename__ = 'vehicles'
    id = Column(Integer, ForeignKey('favorites.id'), primary_key=True)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'vehicle',
    }

render_er(Base, 'diagram.png')

Base.metadata.create_all(engine)


# Create a new user
new_user = User(name="Luke Skywalker")
session.add(new_user)

fav_character = Character(name="Darth Vader")
fav_planet = Planet(name="Tatooine")
fav_vehicle = Vehicle(name="Millennium Falcon")

new_user.favorites.extend([fav_character, fav_planet, fav_vehicle])

session.commit()