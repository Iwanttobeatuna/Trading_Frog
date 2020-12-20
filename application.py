import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

from helpers import apology, login_required, usd

#for stock&indices quote
import investpy
import pandas as pd

#for graph
import json
import plotly
import plotly.graph_objs as go

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route('/')
def home():
    return render_template('home.html')


@app.route("/index")
@login_required
def index():
    """Show portfolio of stocks"""
    site = 'https://finance.yahoo.com/news/rssindex'
    op = urlopen(site) #Open that site
    rd = op.read() #read data from site
    op.close()   # close the object
    sp_page = soup(rd,'xml') #scrapping data from site
    news_list = sp_page.find_all('item') #finding news

    newslist = []
    for news in news_list:
        newsarticle = {
            'title' : news.title.text,
            'link' : news.link.text,
            'date' : news.pubDate.text
        }
        newslist.append(newsarticle)

    t1 = newslist[1]['title']
    l1 = newslist[1]['link']
    d1 = newslist[1]['date']

    t2 =  newslist[2]['title']
    l2 =  newslist[2]['link']
    d2 =  newslist[2]['date']

    t3 =  newslist[3]['title']
    l3 =  newslist[3]['link']
    d3 =  newslist[3]['date']

    t4 =  newslist[4]['title']
    l4 =  newslist[4]['link']
    d4 =  newslist[4]['date']

    t5 =  newslist[5]['title']
    l5 =  newslist[5]['link']
    d5 =  newslist[5]['date']

    t6 =  newslist[6]['title']
    l6 =  newslist[6]['link']
    d6 =  newslist[6]['date']

    t7 =  newslist[7]['title']
    l7 =  newslist[7]['link']
    d7 =  newslist[7]['date']

    t8 =  newslist[8]['title']
    l8 =  newslist[8]['link']
    d8 =  newslist[8]['date']

    t9 =  newslist[9]['title']
    l9 =  newslist[9]['link']
    d9 =  newslist[9]['date']

    sp = investpy.indices.get_index_recent_data(index="S&P 500", country= "United States", as_json=False, order='descending', interval='Daily')
    sp_df = pd.DataFrame(sp, columns=[ "Open", "High", "Low", "Volume", "Currency"])
    op1 = sp_df.iloc[0,0]
    cp1 = sp_df.iloc[1,0]

    nq = investpy.indices.get_index_recent_data(index="	Nasdaq 100", country= "United States", as_json=False, order='descending', interval='Daily')
    nq_df = pd.DataFrame(nq, columns=[ "Open", "High", "Low", "Volume", "Currency"])
    op2 = nq_df.iloc[0,0]
    cp2 = nq_df.iloc[1,0]

    ftuk = investpy.indices.get_index_recent_data(index="FTSE 100", country="United Kingdom", as_json=False, order='descending', interval='Daily')
    ftuk_df = pd.DataFrame(ftuk, columns=[ "Open", "High", "Low", "Volume", "Currency"])
    op3 = ftuk_df.iloc[0,0]
    cp3 = ftuk_df.iloc[1,0]

    hki = investpy.indices.get_index_recent_data(index="FTSE China 50", country="hong kong", as_json=False, order='descending', interval='Daily')
    hki_df = pd.DataFrame(hki, columns=[ "Open", "High", "Low", "Volume", "Currency"])
    op4 = hki_df.iloc[0,0]
    cp4 = hki_df.iloc[1,0]

    ## FTSE Malaysia
    myi = investpy.indices.get_index_recent_data(index="FTSE Malaysia", country="Malaysia", as_json=False, order='descending', interval='Daily')
    myi_df = pd.DataFrame(myi, columns=[ "Open", "High", "Low", "Volume", "Currency"])
    op5 = myi_df.iloc[0,0]
    cp5 = myi_df.iloc[1,0]

    return render_template("index.html",
    t1=t1, l1=l1, d1=d1, t2=t2, l2=l2,d2=d2, t3=t3, l3=l3,d3=d3, t4=t4, l4=l4,d4=d4, t5=t5, l5=l5,d5=d5,t6=t6, l6=l6,d6=d6,t7=t7, l7=l7,d7=d7,t8=t8, l8=l8,d8=d8,
    t9=t9, l9=l9,d9=d9,op1=op1,cp1=cp1, op2=op2, cp2=cp2, op3=op3,cp3=cp3, op4=op4,cp4=cp4,op5=op5,cp5=cp5)

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get username
    username = request.args.get("username")

    # Check for username
    if not len(username) or db.execute("SELECT 1 FROM users WHERE username = ?", username.lower()):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get a stock quote."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("symbol"):
            return apology("missing symbol")

        # Get stock open, high, low, vol
        symbol = request.form.get("symbol")
        df = investpy.get_stock_recent_data(stock=symbol, country='United States', as_json=False, order='descending')
        new_df = pd.DataFrame(df, columns=["Open", "High", "Low", "Volume", "Currency"])
        # Get Description
        description = investpy.get_stock_company_profile(stock=symbol, country='United States', language='english')

        # for stock
        op = new_df.iloc[0,0]
        high = new_df.iloc[0,1]
        low= new_df.iloc[0,2]
        vol= new_df.iloc[0,3]
        currency = new_df.iloc[0,4]

        # for description
        desc=description['desc']
        url=description['url']

        # for graph
        df.to_csv('file.csv',index=True, encoding='utf-8')
        csv_file = 'file.csv'
        df = pd.read_csv(csv_file)

        # Plot graph
        xscale=df["Date"]
        yscale=df["Close"]
        zscale =df["Volume"]
        # Create a trace
        fig = go.Scatter(
            x = xscale,
            y = yscale
            )

        data =[fig]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        # Create a trace
        fig1 = go.Scatter(
            x = xscale,
            y = zscale
            )

        data1 =[fig1]
        graphJSON1 = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)

        # Display quote
        return render_template("quoted.html", tables=[df.to_html(classes='data table table-striped table-hover', header="true")], symbol=symbol,
        op=op,high=high,low=low,vol=vol,currency=currency,desc=desc,url=url,graphJSON=graphJSON,graphJSON1=graphJSON1)

    # GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        try:
            id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                            request.form.get("username"),
                            generate_password_hash(request.form.get("password")))
        except RuntimeError:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/index")

    # GET
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
