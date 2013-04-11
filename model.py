
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import os
import correlation


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

	def similarity(self, other):
		u_ratings = {}
		paired_ratings = []
		for r in self.ratings:
			u_ratings[r.movie_id] = r

		for r in other.ratings:
			u_r = u_ratings.get(r.movie_id)
			if u_r:
				paired_ratings.append( (u_r.rating, r.rating) )

		if paired_ratings:
			return correlation.pearson(paired_ratings)
		else:
			return 0.0

	def predict_rating(self, movie):
		ratings = self.ratings
		other_ratings = movie.ratings
		similarities = [ (self.similarity(r.user), r) for r in other_ratings ]
		similarities.sort(reverse=True)
		similarities = [sim for sim in similarities if sim[0]>0]
		if not similarities: 
			return None
		numerator = sum([r.rating * similarity for similarity, r in similarities])
		denominator = sum([similarity[0] for similarity in similarities])
		return numerator/denominator

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
