from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import datetime
from entities.user_entity import User
from entities.event_entity import Event
from entities.graffity_entity import Graffiti
from entities.leisure_entity import Leisure
from entities.rating_entity import Rating
from entities.user_leisure_entity import UserLeisure

import json

app = Flask(__name__)
CORS(app)
mimetype = 'application/json'

# heroku local web for local run
# Definition of methods for endpoints

current_user = None
logged = False


@app.route('/', methods=['GET', 'POST'])
def start():
    global logged
    logged = False
    if request.method == 'POST':
        email = request.form['email']
        uid = request.form['uid']
        display_name = request.form['displayName']
        profile_picture = request.form['profilePicture']
        user = User.get_by_uid(uid)
        if user is None:
            user = User.create_user(uid, email, display_name, profile_picture)
        global current_user
        current_user = user
        logged = True
        return json.dumps({'status': 'OK'})
    else:
        return render_template('login.html', title='YATAM - Login', logged=logged)


@app.route('/home/', methods=['GET', 'POST'])
def show_home():
    if request.method == 'POST':
        req = request.get_json()
        leisures = Leisure(req).get_all()
        return Response(response=json.dumps(leisures, default=lambda o: o.encode(), indent=4),
                        status=200,
                        mimetype=mimetype)
    else:
        return render_template('home.html', title='YATAM - Home', logged=logged)


@app.route('/map/', methods=['GET', 'POST'])
def show_map():
    if request.method == 'POST':
        req = request.get_json()
        leisures = Leisure(req).get_all()
        return Response(response=json.dumps(leisures, default=lambda o: o.encode(), indent=4),
                        status=200,
                        mimetype=mimetype)
    else:
        return render_template('map.html')


@app.route('/leisure/', methods=['GET'])
def show_leisure():
    idLeisure = request.args.get('id')
    return render_template('leisure.html', id=idLeisure)


@app.route('/leisure/create/', methods=['GET', 'POST'])
def create_leisure():
    if request.method == 'GET':
        return render_template('create_leisure.html', user=current_user)
    elif request.method == 'POST':
        name = request.form['name']
        coordinates = request.form['coordinates']
        description = request.form['description']
        photo = request.form['photo']
        schedule = request.form['schedule']
        address = request.form['address']
        leisure = UserLeisure.create_user_leisure(name=name, coordinates=coordinates, description=description,
                                                  url_photo=photo,
                                                  schedule=schedule, address=address, user=current_user.uid)

        return Response(response=json.dumps({"key": leisure.key}), status=200, mimetype=mimetype)


@app.route('/leisure/user/')
def show_leisure_user():
    keyLeisure = request.args.get('key')
    return render_template('leisure_user.html', key=keyLeisure)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
