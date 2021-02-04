from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, Response, session
from datetime import datetime
from entities.user_entity import User
from entities.event_entity import Event
from entities.graffity_entity import Graffiti
from entities.leisure_entity import Leisure
from entities.rating_entity import Rating
from entities.user_leisure_entity import UserLeisure
from dotenv import load_dotenv

import os
import json

app = Flask(__name__)

load_dotenv()
session_key = os.getenv('sessionPrivateKey')
app.secret_key = session_key

CORS(app)
mimetype = 'application/json'

# heroku local web for local run
# Definition of methods for endpoints

'''
How to use session data:

Get session data:
data = session['dataName']
data = session.get('dataName')

Set session data:
session['dataName'] = data

Remove session data:
session.pop('dataName', None)

Check if data is created in session:
if 'dataName' in session:
'''


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':  # when an user enters with Google
        email = request.form['email']
        uid = request.form['uid']
        display_name = request.form['displayName']
        profile_picture = request.form['profilePicture']
        user = User.get_by_uid(uid)
        if user is None:
            User.create_user(uid, email, display_name, profile_picture)
        session['current_user_email'] = email
        session['current_user_uid'] = uid
        session['current_user_display_name'] = display_name
        session['current_user_profile_picture'] = profile_picture
        return json.dumps({'status': 'OK'})
    else:
        if 'current_user_uid' in session:
            return redirect(url_for('show_home'))
        else:
            return render_template('login.html', title='YATAM - Login')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('current_user_email', None)
    session.pop('current_user_uid', None)
    session.pop('current_user_display_name', None)
    session.pop('current_user_profile_picture', None)

    return redirect(url_for('start'))


@app.route('/home', methods=['GET', 'POST'])
def show_home():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        if request.method == 'POST':
            req = request.get_json()
            leisures = Leisure(req).get_all()
            return Response(response=json.dumps(leisures, default=lambda o: o.encode(), indent=4),
                            status=200,
                            mimetype=mimetype)
        else:
            return render_template('home.html', title='YATAM - Home')


@app.route('/map', methods=['GET', 'POST'])
def show_map():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        if request.method == 'POST':
            req = request.get_json()
            if req == "USERLEISURE":
                leisures = UserLeisure.get_all()
            else:
                leisures = Leisure(req).get_all()
            return Response(response=json.dumps(leisures, default=lambda o: o.encode(), indent=4),
                            status=200,
                            mimetype=mimetype)
        else:
            return render_template('map.html', title='YATAM - Map')


@app.route('/profile', methods=['GET'])
def show_profile():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        return render_template('profile.html', title='YATAM - My Profile')


@app.route('/changeDisplayName', methods=['POST'])
def change_display_name():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        req = request.get_json()
        User.change_display_name(session['current_user_uid'], req)
        session.pop('current_user_display_name', None)
        session['current_user_display_name'] = req['displayName']
        return redirect(url_for('show_profile'))


@app.route('/graffities', methods=['GET'])
def show_leisures_user():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        return render_template('graffiti_list.html', title='YATAM - Graffities')


@app.route('/leisuresFromUsers', methods=['GET'])
def show_graffities():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        return render_template('leisures_user.html', title='YATAM - Leisures From Users')


@app.route('/leisure', methods=['GET'])
def show_leisure():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        l_type = request.args.get('type')
        l_Id = int(request.args.get('id'))
        leisure = Leisure(l_type).get_by_id(l_Id)
        ratings = Rating.get_ratings_by_leisure('leisure', l_Id)
        return render_template('leisure.html', l=leisure, ratings=ratings, title='YATAM - ' + leisure.name)


@app.route('/saverating', methods=['GET', 'POST'])
def save_rating():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        if request.method == 'POST':
            r_Id = request.form['id']
            grade = int(request.form['grade'])
            description = request.form['description']
            l_Id = int(request.form['leisure'])
            l_type = request.form['type']
            user = session['current_user_uid']
            if r_Id == 'null':
                Rating.create_rating(grade, description, l_Id, user)
            else:
                data = {"grade": grade, "description": description}
                Rating.update_rating(r_Id, data)
            return redirect(url_for('show_leisure', id=l_Id, type=l_type))


@app.route('/deleterating', methods=['GET', 'POST'])
def delete_rating():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        r_Id = request.form['id']
        l_Id = int(request.form['leisure'])
        l_type = request.form['type']
        Rating.delete_rating(r_Id)
        return redirect(url_for('show_leisure', id=l_Id, type=l_type))


@app.route('/leisure/create', methods=['GET', 'POST'])
def create_leisure():
    leisure = None
    if 'current_user_uid' not in session:
        redirect(url_for('start'))
    else:
        if request.method == 'GET':
            return render_template('create_leisure.html')
        elif request.method == 'POST':
            name = request.form['name']
            coordinates = request.form['coordinates']
            coordinates = coordinates.split(',')
            description = request.form['description']
            photo = request.form['photo']
            schedule = request.form['schedule']
            address = request.form['address']
            leisure = UserLeisure.create_user_leisure(name=name, coordinates=coordinates, description=description,
                                                      url_photo=photo,
                                                      schedule=schedule, address=address,
                                                      user=session['current_user_uid'])
        if leisure is not None:
            return Response(response=json.dumps({"key": leisure.key}), status=200, mimetype=mimetype)


@app.route('/graffity/create', methods=['GET', 'POST'])
def create_graffity():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        if request.method == 'GET':
            return render_template('create_graffity.html', title='YATAM - Create Graffiti')
        elif request.method == 'POST':
                description = request.form['description']
                photo = request.form['photo']
                graffity = Graffiti.create_graffiti(description=description, url=photo, user=session['current_user_uid'])
        return redirect(url_for('show_graffity', key = graffity.key))

@app.route('/graffity')
def show_graffity():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        key = str(request.args.get('key'))
        graffity = Graffiti.get_by_key(key)
        description = graffity.description
        nlikes = graffity.n_likes
        return render_template('graffity.html', description = description, nlikes = nlikes)


@app.route('/leisure/user')
def show_leisure_user():
    key_leisure = request.args.get('key')
    return render_template('leisure_user.html', key=key_leisure)


@app.route('/events', methods=['GET'])
def show_events():
    if 'current_user_uid' not in session:
        return redirect(url_for('start'))
    else:
        return render_template('events.html', title='YATAM - Events 2020')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)