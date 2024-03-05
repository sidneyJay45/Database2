from flask import Flask, render_template, request , redirect , url_for , session , flash
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=1)


db = SQLAlchemy(app)

#define class represents the user objects(inside the database)
class users(db.Model):
  _id = db.Column("id", db.Integer, primary_key=True)  
  name = db.Column(db.String(100))  # Fix: Change db.string to db.String
  password = db.Column(db.String(100))

  def __init__(self, name, password):
    self.name = name
   
    self.password = password

@app.route ("/")
def home():
  return render_template("home.html")



#use of sessions avoid logging in again and again
@app.route('/login', methods=["POST" , "GET"])
def login():
  if request.method == "POST":
     user = request.form["nm"]
    
     third = request.form["password"]
     session["user"] = user
     
     session["third"] = third

     found_user = users.query.filter_by(name=user).first()
     if found_user:
       if found_user.password == third:
         flash("Logged in successfully")
         return redirect(url_for("user"))
     else:
         usr = users(user, third)
         db.session.add(usr)
         db.session.commit()
     return redirect(url_for("user"))
  else:
     if "user" in session:
         return redirect(url_for("user"))
     return render_template("login.html")


@app.route("/user" , methods=["POST","GET"])
def user():
   if "user" in session:
      user = session ["user"]

      if request.method =="POST":
         password = request.form["password"]
         session["password"] = password
         found_user = users.query.filter_by(name=user).first()
         found_user.password = password
         db.session.commit()
         flash('password saved successfully')
      return f"<h1>{user}</h1>"
   else:
      return redirect(url_for("login"))

#delete all session data by adding the logout
# use of flash messages for the logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out!")
    return redirect(url_for("login"))


@app.route("/view")
def view():
  return render_template('view.html', values= users.query.all())


with app.app_context():
  db.create_all()


if __name__ == "__main__":

   app.run(host = '0.0.0.0',debug= True)


