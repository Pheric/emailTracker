from flask import Flask, request, redirect, make_response, render_template

import account
import db
import utils

app = Flask(__name__)
# username: secret
sessions = {}


@app.route("/", methods=["GET"])
def handleIndex():
    return app.send_static_file("index.html")


@app.route("/loginfailed", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def handleLogin():
    if request.method == "GET":
        if checkAuthed(request):
            return redirect("/view")
        return app.send_static_file("login.html")
    else:
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            return redirect("/loginfailed")

        if db.checkAcct(username, password):
            secret = utils.genSalt()
            sessions[username] = secret

            resp = make_response(redirect("/view"))
            # this cookie stuff was a major pain... expires != max_age
            resp.set_cookie('username', username, max_age=600, path='/')
            resp.set_cookie('secret', secret, max_age=600, path='/')
            return resp
        else:
            return redirect("/loginfailed")


@app.route("/registerfailed", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def handleRegister():
    if request.method == "GET":
        if checkAuthed(request):
            return redirect("/view")
        return app.send_static_file("register.html")
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username == '' or password == '' or email == '':
            return redirect("/registerfailed")

        acct = account.Account(username, password, email)
        if db.insertAcct(acct):
            return redirect("/login")
        else:
            return redirect("/registerfailed")


@app.route("/view", methods=["GET", "POST"])
def handleView():
    if not checkAuthed(request):
        return redirect("/login")
    hits = []
    tracker = ""
    print(request.values)
    if 'trackers' in request.values:
        tracker = request.values['trackers']
        print(tracker)
        hits = db.selectHits(tracker, request.cookies['username'])
    return render_template('view.html', username=request.cookies['username'], trackers=db.selectUserTrackers(request.cookies['username']), hits=hits, tracker=tracker)


def checkAuthed(req):
    return 'username' in req.cookies and 'secret' in req.cookies\
        and req.cookies['username'] in sessions and\
           sessions[req.cookies['username']] == req.cookies['secret']
