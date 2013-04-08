from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable=True)
	password = Column(String(64), nullable=True)
	age = Column(Integer, nullable=True)
	zipcode = Column(String(15), nullable=True)

	# def __init__(self, email = None, password = None, age=None, zipcode=None):
	# 	self.email = email
	# 	self.password = password
	# 	self.age = age
	# 	self.zipcode = zipcode

class Movie(Base):
	__tablename__ = "movies"

	id = Column(Integer, primary_key = True)
	name = Column(String(64), nullable=True)
	released_at = Column(String(64), nullable=True)
	imbd_url = Column(String(64), nullable=True)

	# def __init__(self, name = None, released_at = None, imbd_url=None):
	# 	self.name = name
	# 	self.released_at = released_at
	# 	self.imbd_url = imbd_url

class Rating(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	movie_id = Column(Integer, ForeignKey('movies.id'))
	user_id = Column(Integer, ForeignKey('users.id'))
	rating = Column(Integer, nullable=True)

	user = relationship("User", backref=backref("ratings", order_by=id))
	movie = relationship("Movie", backref=backref("ratings", order_by=id))

	# def __init__(self, movie_id = None, user_id = None, rating = None):
	# 	self.movie_id = movie_id
	# 	self.user_id = user_id
	# 	self.rating = rating

### End class declarations

# def connect():
# 	global Engine
# 	global Session

# 	Engine = create_engine("sqlite:///ratings.db", echo=True)
# 	Session = sessionmaker(bind=Engine)

# 	return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
