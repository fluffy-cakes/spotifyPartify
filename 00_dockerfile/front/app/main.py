import flask
import flask_login
import flask_sqlalchemy
import json
import requests
import urllib.parse


login_manager = flask_login.LoginManager()
db            = flask_sqlalchemy.SQLAlchemy()



class User(flask_login.UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)



def is_safe_url(target):
    ref_url  = urllib.parse.urlparse(flask.request.host_url)
    test_url = urllib.parse.urlparse(urllib.parse.urljoin(flask.request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc




app = flask.Flask(__name__)
app.config['SECRET_KEY']                     = 'secret'
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager.init_app(app)
login_manager.login_view = 'login'
db.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/', methods=['GET'])
@flask_login.login_required
def getUI():
    return flask.render_template('index.html')



# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        user     = User.query.filter_by(username=username).first()

        if not user:
            return '<h1>Computer says no.</h1>'

        flask_login.login_user(user, remember=True)

        if 'next' in flask.session and flask.session['next']:
            if is_safe_url(flask.session['next']):
                return flask.redirect(flask.session['next'])
        return flask.redirect(flask.url_for('getUI'))

    flask.session['next'] = flask.request.args.get('next')
    return flask.render_template('login.html')



@app.route('/login/<id>', methods=['GET'])
def autoLogin(id):
    user = User.query.filter_by(username=id).first()
    flask_login.login_user(user, remember=True)

    if not user:
        return '<h1>Computer says no.</h1>'

    if 'next' in flask.session and flask.session['next']:
        if is_safe_url(flask.session['next']):
            return flask.redirect(flask.session['next'])
    return flask.redirect(flask.url_for('getUI'))



@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('getUI'))



# API
@app.route('/api/currenttrack', methods=['GET'])
@flask_login.login_required
def apiCurrenttrack():
    response = requests.get('http://127.0.0.1:5000')
    return response.text



@app.route('/api/downvote', methods=['POST'])
@flask_login.login_required
def apiDownvote():
    requests.post('http://127.0.0.1:5000/api/downvote')
    return json.dumps(True)



@app.route('/api/upvote', methods=['POST'])
@flask_login.login_required
def apiUp():
    requests.post('http://127.0.0.1:5000/api/upvote')
    return json.dumps(True)



# API ADMIN
@app.route('/admin', methods=['GET', 'POST'])
@flask_login.login_required
def admin():
    user = User.query.filter_by(id=flask.session["_user_id"]).first()

    if user.username.startswith("admin_"):
        if flask.request.method == 'POST':
            votelimit = flask.request.form.get('votelimit')
            votetime  = flask.request.form.get('votetime')

            if votelimit != "":
                requests.post('http://127.0.0.1:5000/admin/limit/{}'.format(int(votelimit)))
            if votetime != "":
                requests.post('http://127.0.0.1:5000/admin/time/{}'.format(int(votetime)))
            if 'next' in flask.session and flask.session['next']:
                if is_safe_url(flask.session['next']):
                    return flask.redirect(flask.session['next'])
            return flask.redirect(flask.url_for('getUI'))
        return flask.render_template('admin.html')
    else:
        return '<h1>Computer says no.</h1>'



@app.route('/admin/check', methods=['GET'])
@flask_login.login_required
def adminCheck():
    user = User.query.filter_by(id=flask.session["_user_id"]).first()

    if user.username.startswith("admin_"):
        return json.dumps(True)
    else:
        return json.dumps(False)



@app.route('/admin/over', methods=['GET'])
@flask_login.login_required
def adminOver():
    user = User.query.filter_by(id=flask.session["_user_id"]).first()

    if user.username.startswith("admin_"):
        requests.get('http://127.0.0.1:5000/admin/over')
        return json.dumps(True)
    else:
        return json.dumps(False)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)