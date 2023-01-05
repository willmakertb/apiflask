import requests
from flask import render_template, session, redirect, flash, url_for, jsonify, request
from app.forms import LoginForm
#from app.firestore_service import get_user, user_put
#from app.models import UserModel, UserData
from flask_login import login_user,  login_required, logout_user
#from werkzeug.security import generate_password_hash, check_password_hash

from .model import get_users
from . import auth
from app.models import UserData, UserModel
#login_manager = LoginManager()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    user_doc = []
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_users(username)
        if user_doc.to_dict() is not None:
            print(user_doc.to_dict())
            password_from_db = user_doc.to_dict()['password']
            print(password_from_db)
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
            else:
                res = {
                    'Error': "informacion no concide"
                }
                return res
        else:
            res = {
                'Error': "El usuario no exite"
                }
            return res


        return jsonify(user_doc)

    return render_template('login.html', **context)


@auth.route('/signup')
def signup():
    return 'Signup'


@auth.route('/logout')
def logout():
    return 'Logout'




''' 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)
        print(user_doc)
        if user_doc.to_dict() is not None:
            print(user_doc.to_dict())
            password_from_db = user_doc.to_dict()['password']
            print(password_from_db)
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')

                redirect(url_for('hello'))

            else:
                flash('La informacion no coincide ')

        else:
            flash('El usuario no existe ')


        flash('Nombre de usario registrado con éxito!')

        return redirect(url_for('index'))

    return render_template('login.html', **context)

@auth.route('/newlogin', methods=['GET', 'POST'])
def newlogin():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)
        print(user_doc)
        if user_doc.to_dict() is not None:
            print(user_doc.to_dict())
            password_from_db = user_doc.to_dict()['password']
            print(password_from_db)
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')

                redirect(url_for('hello'))

            else:
                flash('La informacion no coincide ')

        else:
            flash('El usuario no existe ')


        flash('Nombre de usario registrado con éxito!')

        return redirect(url_for('index'))

    return render_template('loginbootstrap.html', **context)


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        #user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)

            flash('Bienvenido')

            return redirect(url_for('hello'))

        else:
            flash('El usuario ya existe!')

    return render_template('signup.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()

    flash('Regresa pronto ')
    return redirect(url_for('auth.login'))



'''
