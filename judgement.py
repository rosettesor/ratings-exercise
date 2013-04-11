
from flask import Flask, render_template, redirect, request, session, url_for
import model

app = Flask(__name__)
app.secret_key = "obligatory_secret_key"

@app.route("/")
def index():
	# return "Hello world!"
	user_list = model.session.query(model.User).limit(10).all()
	return render_template("user_list.html", users=user_list)

@app.route("/ratings/<id>") #get all ratings by particular user id
def user_ratings(id=None):
	user_ratings = model.session.query(model.Rating).filter_by(user_id=id).all()
	return render_template("user_ratings.html", ratings=user_ratings)

@app.route("/new_user")
def create_user():
	return render_template("new_user.html")

@app.route("/save_user", methods=["POST"])
def save_user():
	new_email = request.form['email']
	new_password = request.form['password']
	new_age = request.form['age']
	new_zipcode = request.form['zipcode']
	new_user = model.User(email = new_email, password = new_password, age = new_age, zipcode = new_zipcode)
	model.session.add(new_user)
	model.session.commit()
	return redirect("/")

@app.route("/movie/<int:id>",  methods = ["GET", "POST"])
def view_movie(id):
	movie = model.session.query(model.Movie).get(id)
	ratings = movie.ratings
	rating_nums = []
	user_rating = None
	for r in ratings:
		if r.user_id == session['id']:
			user_ratingr = r
		rating_nums.append(r.rating)
	avg_rating = float(sum(rating_nums))/len(rating_nums)

	# prediction code: only predict if the user hasn't rated yet
	user = model.session.query(model.User).get(session['id'])
	prediction = None
	if not user_rating:
		prediction = user.predict_rating(movie)
		effective_rating = prediction
	else:
		effective_rating = user_rating.rating
	# end prediction

	#now including the eye's opinion
	the_eye = model.session.query(model.User).filter_by(email="theeye@ofjudgement.com").one()
	eye_rating = model.session.query(model.Rating).filter_by(user_id=the_eye.id, movie_id=movie.id).first()
	if not eye_rating:
		eye_rating = the_eye.predict_rating(movie)
	else:
		eye_rating = eye_rating.rating
	difference = abs(eye_rating - effective_rating)

	messages = [ "I suppose you don't have such bad taste after all.",
             "I regret every decision that I've ever made that has brought me to listen to your opinion.",
             "Words fail me, as your taste in movies has clearly failed you.",
             "That movie is great. For a clown to watch. Idiot."]
	beratement = messages[int(difference)]
	return render_template("movie.html", movie = movie, average = avg_rating, user_rating = user_rating, prediction = prediction, beratement = beratement)

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/again_login")
def again_login():
	return render_template("again_login.html")

@app.route("/login_user", methods = ["POST"])
def login_user():
	user_email = request.form['email']
	user_password = request.form['password']
	find_user = model.session.query(model.User).filter_by(email=user_email, password=user_password).first()
	if find_user:
		session['email']=user_email
		session['id']=find_user.id
		return redirect("/")
	else:
		return redirect("/again_login")

@app.route("/my_ratings")
def my_ratings():
	my_ratings = model.session.query(model.Rating).filter_by(user_id=session['id']).all()
	return render_template("my_ratings.html", mine = my_ratings)

@app.route("/change_rating", methods = ["POST"])
def change_rating():
	movie_change = request.form['movie_name']
	find_movie = model.session.query(model.Movie).filter_by(name=movie_change).first()
	rating_change = request.form['new_rating']
	current_rating = model.session.query(model.Rating).filter(model.Rating.user_id==session['id'], model.Rating.movie_id==find_movie.id).first()
	current_rating.rating = rating_change
	model.session.commit()
	return redirect("/my_ratings")

if __name__ == "__main__":
	app.run(debug = True)