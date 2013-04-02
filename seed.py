import model
import csv

def load_users(session):
    # use u.user
    with open('u.user', 'rb') as f:
        reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        for row in reader:
            print row

def load_movies(session):
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)

load_users