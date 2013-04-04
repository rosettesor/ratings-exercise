import model
import csv
from datetime import date, time, datetime

# open a file - YAY!
# read a line - YAY!
# parse a line - YAY!
# create an object - YAY!
# add the object to a session - YAY!
# commit - YAY!
# repeat until done - YAY!

def load_users(session):     
    # use u.user   
    with open('seed_data/u.user') as f:
        reader = csv.reader(f, delimiter='|')  
        for row in reader: 
            user = model.User(age=row[1], zipcode=row[4], id=row[0])
            session.add(user)  

def load_movies(session):
    # use u.item
    with open('seed_data/u.item') as f:
        reader = csv.reader(f, delimiter='|')
        date_format = '%d-%b-%Y'
        for row in reader:
            movie = model.Movie(id=row[0], imbd_url=row[4])
            formatted_title = row[1]
            formatted_title = formatted_title.decode("latin-1")
            movie.name = formatted_title
            date_string = row[2]
            if date_string:
                formatted_date = datetime.strptime(date_string, date_format)
                movie.released_at = formatted_date
            else:
                None
            session.add(movie)

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        for row in reader:
            rating = model.Rating(movie_id=row[1], user_id=row[0], rating=row[2])
            session.add(rating)

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)
    session.commit()

if __name__ == "__main__":
    s= model.connect()
    main(s)