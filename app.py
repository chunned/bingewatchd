from flask import Flask,url_for,request,render_template,session,redirect
app = Flask(__name__)
from main import *
import tmdb
import db
import bcrypt
#import dotenv
import os

#make a secrets app key for sesions
#secrets = dotenv.dotenv_values('.env')
#secretKey = secrets["SECRET_KEY"]
#app.secret_key = f"{secretKey}"
app.secret_key = os.getenv("SECRET_KEY")
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

@app.route("/404")
def returnError():
    return render_template("404.html",token=session.get("token"))

@app.route("/mylist",methods=["POST","GET"])
def view():
    try : 
        getEpisodesData = getEpisodes()
        print(getEpisodesData)
        return render_template("list.html",eps=getEpisodesData,token=session.get("token"))
    except: 
        return render_template("list.html",token=session.get("token"))

@app.route("/search_episode",methods=["POST","GET"])
def getNewEpisode():
    allShows = tmdb.searchShow(request.form.get("show_name"))
    return render_template("select_show.html",token=session.get("token"),data=allShows,show_name=request.form.get("show_name"))

@app.route("/add_details",methods=["POST","GET"])
def addShowDetails():
    try : 
        if request.form.get("selected_show") == None:
            return redirect("/404") #add 404 page here, redirects to index atm
        return render_template("add_details.html",token=session.get("token"),id=request.form.get("selected_show"),show_name=request.form.get("hidden_show_name"))
    except:
        return redirect("/404")

@app.route("/add_show",methods=["POST","GET"])
def addShow():
    try : 
        data = tmdb.searchShow(request.form.get("show_name"))
        show = data['results'][int(request.form.get('show_id'))-1]
        id = show['id']
        seasonNum = request.form.get("season_num")
        epNum = request.form.get("episode_num")
        myRating = request.form.get("my_rating")
        watchDate = request.form.get("watchd_date")
        newEpisodes = newEpisode(int(id),int(seasonNum),int(epNum),int(myRating),watchDate)
        return redirect("/mylist")
    except:
        return redirect("/404")

@app.route("/add",methods=["POST","GET"])
def add():
    return render_template("add.html",token=session.get("token"))

@app.route("/update",methods=["GET","POST"])
def update():
    return render_template("update.html",token=session.get("token"),id=request.form.get("new_episode_id"))

@app.route("/delete",methods=["POST"])
def deleteTableEntry():
    try : 
        deleteEntry("show_season",request.form.get("show_id"))
        deleteEntry("season",request.form.get("season_id"))
        deleteEntry("episode",request.form.get("episode_id"))
        return redirect("/mylist")
    except:
        return redirect("/404")

@app.route("/put_update",methods=["POST"])
def patchEntry():
    print(request.form.get("episode_id"))
    print(request.form.get("new_watchd_date"))
    newRating = request.form.get("new_my_rating")
    if newRating == "":
        newRating = "N/A"
    patchInstance("episode",request.form.get("episode_id"),
    request.form.get("new_watchd_date"),newRating)
    return redirect("/mylist")


@app.route("/login",methods=["POST","GET"])
def login():
    return render_template("login.html",token=session.get("token"))

@app.route("/register",methods=["POST","GET"])
def register():
    return render_template("register.html",token=session.get("token"))

@app.route("/logout",methods=["POST","GET"])
def logout():
    session["token"] = None
    return redirect("/")

@app.route("/submit_login",methods=["POST","GET"])
def submit_login():
    name = request.form.get("username")
    passwd = request.form.get("password")
    userdb = ulogin(cursor, connection,name,passwd)
    if (userdb == None) or (name == "") or (passwd == ""):
        session["token"] = None
        return render_template("login.html",token=session.get("token"))
    session["token"] = userdb
    con = sqlite3.connect(session.get("token"))
    cur = con.cursor()
    db.createTables(cur)
    print('Database created successfully.')
    return redirect("/")

@app.route("/submit_register",methods=["POST","GET"])
def submit_register():
    try : 
        name = request.form.get("username")
        passwd = request.form.get("password")
        if (name == "") or (passwd == ""):
            raise Exception
        createUser = new_user(cursor, connection,name,passwd)
        session["token"] = createUser
        return redirect("/login")
    except: 
        return redirect("/404")

if __name__ == '__main__':
    app.run(host="localhost", debug=True, port=6969)
