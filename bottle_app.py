from bottle import default_app, route, template, get, post, request, run
import sqlite3
import bottle_sqlite

db = sqlite3.connect("./testdb.db")
c = db.cursor()

###########################################

# HANDLES DISPLAYING THE /getInput PAGE
@route('/')
@get('/getInput')
def getInput():
    return template("getInput.html")


# HANDLES PROCESSING THE FORM ON THE /getInput PAGE AFTER THE USER CLICKS SUBMIT
@post('/getInput')
def doInput():
    txtField = request.forms.get('txtField')
    passField = request.forms.get('passField')
    return template("doInput.html", txtField=txtField, passField=passField, db=db, c=c)

@route('/login')
def GETLogin():
    txtField = request.forms.get('txtField')
    passField = request.forms.get('passField')

    sql = "SELECT * FROM users WHERE id = 5 or 1=1"
    c.execute(sql)
    res = c.fetchall()

    db.commit()

    return template("login.html", db=db, c=c, res=res)

@post('/login')
def POSTLogin():
    txtField = request.forms.get('txtField')
    passField = request.forms.get('passField')

    sql = "SELECT * FROM users WHERE name = '" + txtField + "' AND password = '" + passField + "'"
    print(sql)
    res = c.execute(sql)
    db.commit()

    return template("login.html", db=db, c=c, res=res)

# HANDLES RESETTING THE DATABASE WITH DEFAULT USERS AND PASSWORDS
@route('/resetDB')
def resetDB():

    c.execute('DROP TABLE IF EXISTS users')
    sqlScript = '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name VARCHAR (255),
        password VARCHAR (255)
    ) '''

    c.execute(sqlScript)
    db.commit()

    c.execute("INSERT INTO users VALUES (null, ?, ?)", ("admin", "Pa$$w0rd"))
    c.execute("INSERT INTO users VALUES (null, ?, ?)", ("just_a_guy", "s3cr3t"))
    db.commit()

    return template("resetDB.html", db=db, c=c)


# HANDLES VIEWING THE DATABASE
@route('/viewDB')
def viewDB():
    return template("viewDB.html", db=db, c=c)


application = default_app() #not sure what this does but everything breaks without it :)

run()