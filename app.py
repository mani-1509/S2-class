from flask import Flask, request, jsonify, render_template, redirect, url_for,send_from_directory , session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'mani1509'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    tracking_data = db.Column(db.Text, nullable=True)  

with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error="Username already exists")
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

# @app.route('/test')
# def test():
#     return render_template('3Dtest.html')

# @app.route('/static/<path:path>')
# def static_proxy(path):
#     if path.endswith('.js'):
#         return send_from_directory('static', path, mimetype='application/javascript')
#     return send_from_directory('static', path)

# @app.route('/node_modules/<path:path>')
# def node_modules(path):
#     return send_from_directory('node_modules', path)

if __name__ == "__main__":
    app.run(debug=True)
