import json
from flask import Blueprint, render_template, redirect, url_for, abort, request, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.security import generate_password_hash, check_password_hash
from dealeumApp import db
from dealeumApp.models.user import User
from dealeumApp.models.deal import Deal

auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        
        # TODO
        username = request.form.get('username')
        pwd = request.form.get('password')
        if not username:
            flash("Username field is empty",'fail')
            return redirect(url_for('auth.login'))
        if not pwd:
            flash("Password field is empty",'fail')
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User not found','fail')
            return redirect(url_for('auth.login'))
        if check_password_hash(user.password,pwd):
            flash('Logged in', 'success')
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash("Password doesn't match",'fail')
            return redirect(url_for('auth.login'))
        
    
    next = request.args.get('next')
    return render_template('accounting/login.html',next=next)



@auth.route('/register',methods=['GET','POST'])
def signup():
    print("XXX")
    if request.method == 'GET':
        print("XXX")
        return render_template('accounting/register.html')
    else:
        print("XX")
        print(request.form)
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        print("XXX")
        if email == None or username == None or password == None:
            flash("Please fill all the fields")
            return render_template('accounting/register.html')
        print("XXX")
        user = User.query.filter_by(email=email).first()
        print("XXX")
        if user:
            flash("This email has already an account")
            return render_template('accounting/register.html')
        print("XXX")
        user = User.query.filter_by(username=username).first()
        print("XXX")
        if user:
            flash("This username has been taken")
            return render_template('accounting/register.html')
        print("XXX")

        new_user = User(email=email, username=username, password=generate_password_hash(password,method='sha256'))
        flash("An account has been created")
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        print("user commited")

        return redirect(url_for('auth.login'))


@auth.route('/profile/<string:username>')
def profile(username):
    print(username)
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('accounting/profile.html',profile_user=user)
    else:
        return jsonify({"error":"Page not found"}),404



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@auth.route('/changepass',methods=['PUT'])
@login_required
def changepassword():
    # TODO
    pass