# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:15:49 2023

@author: abc
"""

from flask import Flask, render_template,request,session
import ibm_db

app = Flask(__name__)
app.secret_key = "_ab+d=5"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;UID=cwh28378;PWD=g7DA8KRWkGhDnGWB;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt", '','')
print(ibm_db.active(conn))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global uname
        uname = request.form['username']
        pword = request.form['password']
        print(uname, pword)
        sql = "SELECT * FROM REGISTER WHERE USERNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt,2,pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            session['username'] = uname
            session['emailid'] = out['EMAILID']
            if out['ROLE'] == 0:
                return render_template("adminprofile.html",adname = out['NAME'], ademail = out['EMAILID'] )
            elif out['ROLE'] == 1:
                return render_template("studentprofile.html", sname= out['NAME'],semail = out['EMAILID'])
            else: 
                return render_template("facultyprofile.html", fname = out['NAME'],femail = out['EMAILID'])
        else: 
            msg = "Invalid Credentials"
            return render_template("login.html",msg= msg)
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        uname = request.form['uname']
        pword = request.form['password']
        role = request.form['role']
        print(uname,email,pword,role)
        sql = "SELECT * FROM REGISTER WHERE USERNAME=? and EMAILID=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt, 2, email)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            msg = "Already Registered"
            return render_template("register.html",msg = msg)
        else:
            sql = "INSERT INTO REGISTER VALUES(?,?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2,email)
            ibm_db.bind_param(stmt, 3, uname)
            ibm_db.bind_param(stmt, 4, pword)
            ibm_db.bind_param(stmt, 5, role)
            ibm_db.execute(stmt)
            msg = "Registered"
            return render_template("register.html", msg =msg)

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)