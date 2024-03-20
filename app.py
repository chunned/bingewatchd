from flask import Flask,url_for,request,render_template,session,redirect
app = Flask(__name__)
from main import *
import tmdb
import db
import bcrypt
import dotenv

#make a secrets app key for sesions
secrets = dotenv.dotenv_values('.env')
secretKey = secrets["SECRET_KEY"]
app.secret_key = f"{secretKey}"

#initialize the user.db connection
USER_DB = "users.db"
# Initialize user database
connection = sqlite3.connect(USER_DB, check_same_thread=False)
cursor = connection.cursor()

#routes for the default pages, e.g. home, search page
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html",token=session.get("token"))

@app.route("/mylist",methods=["POST","GET"])
def view():
    try : 
        getEpisodesData = getEpisodes()
        print(getEpisodesData)
    except: 
        return render_template("list.html",token=session.get("token"))
    return render_template("list.html",eps=getEpisodesData,token=session.get("token"))

@app.route("/search_episode",methods=["POST","GET"])
def getNewEpisode():
    allShows = tmdb.searchShow(request.form.get("show_name"))
    return render_template("select_show.html",token=session.get("token"),data=allShows,show_name=request.form.get("show_name"))

@app.route("/add_details",methods=["POST","GET"])
def addShowDetails():
    if request.form.get("selected_show") == None:
        return redirect("/") #add 404 page here, redirects to index atm
    return render_template("add_details.html",token=session.get("token"),id=request.form.get("selected_show"),show_name=request.form.get("hidden_show_name"))

@app.route("/add_show",methods=["POST","GET"])
def addShow():
    data = tmdb.searchShow(request.form.get("show_name"))
    show = data['results'][int(request.form.get('show_id'))-1]
    id = show['id']
    seasonNum = request.form.get("season_num")
    epNum = request.form.get("episode_num")
    myRating = request.form.get("my_rating")
    newEpisodes = newEpisode(int(id),int(seasonNum),int(epNum),int(myRating))
    return redirect("/mylist")

@app.route("/add",methods=["POST","GET"])
def add():
    return render_template("add.html",token=session.get("token"))

@app.route("/login",methods=["POST","GET"])
def login():
    return render_template("login.html",token=session.get("token"))

@app.route("/register",methods=["POST","GET"])
def register():
    return render_template("register.html",token=session.get("token"))

@app.route("/logout",methods=["POST","GET"])
def logout():
    session["token"] = None
    return render_template("index.html",token=session.get("token"))

@app.route("/submit_login",methods=["POST","GET"])
def submit_login():
    name = request.form.get("username")
    passwd = request.form.get("password")
    userdb = ulogin(cursor, connection,name,passwd)
    if userdb == None:
        session["token"] = None
        return render_template("login.html",token=session.get("token"))
    session["token"] = userdb
    con = sqlite3.connect(session.get("token"))
    cur = con.cursor()
    db.createTables(cur)
    print('Database created successfully.')
    return render_template("index.html",token=session.get("token"))

@app.route("/submit_register",methods=["POST","GET"])
def submit_register():
    name = request.form.get("username")
    passwd = request.form.get("password")
    createUser = new_user(cursor, connection,name,passwd)
    session["token"] = createUser
    return render_template("index.html",token=session.get("token"))

if __name__ == '__main__':
    app.run(host="localhost", debug=True, port=6969)