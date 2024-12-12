from flask import Flask, request, jsonify, render_template, redirect, url_for,send_from_directory , session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room, leave_room
from models.model_1 import generate_response

app = Flask(__name__)
app.secret_key = 'mani1509'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    interests = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), default='offline')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    logged_in = 'user_id' in session
    user = None
    if logged_in:
        user = User.query.get(session['user_id'])
    return render_template('index.html', logged_in=logged_in , user=user)

@app.route('/bot')
def bot():
    logged_in = 'user_id' in session
    user = None
    if logged_in:
        user = User.query.get(session['user_id'])
    return render_template('bot.html', logged_in=logged_in , user=user)

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Please enter a valid message."})

    # Prepare prompt
    prompt = f"User: {user_message}\nChatBot:"
    response = generate_response(prompt)
    return jsonify({"response": response})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('edit_profile'))
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
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    

    logged_in = 'user_id' in session
    user = None
    if logged_in:
        user = User.query.get(session['user_id'])    

    user = User.query.get(session['user_id'])
    if user:
        skills = user.skills.split(",") if user.skills else []
        interests = user.interests.split(",") if user.interests else []
        return render_template('profile.html', user=user, skills=skills, interests=interests , logged_in=logged_in)
    return redirect(url_for('home'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    logged_in = 'user_id' in session
    user = None
    if logged_in:
        user = User.query.get(session['user_id'])

    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.bio = request.form['bio']
        user.skills = request.form['skills']
        user.interests = request.form['interests']
        profile_image = request.files['profile_image']
        
        if profile_image:
            image_path = f'static/images/{user.username}_profile.jpg'
            profile_image.save(image_path)
            user.profile_image = image_path.replace("static/", "")

        db.session.commit()
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', user=user , logged_in=logged_in)


@app.route('/chat/<int:receiver_id>')
def chat(receiver_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    

    logged_in = 'user_id' in session
    user = None
    if logged_in:
        user = User.query.get(session['user_id'])

    current_user_id = session['user_id']
    receiver = User.query.get(receiver_id)
    
    messages = Message.query.filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == receiver_id)) |
        ((Message.sender_id == receiver_id) & (Message.receiver_id == current_user_id))
    ).order_by(Message.timestamp).all()
    
    return render_template('chat.html', messages=messages, receiver=receiver , user=user , logged_in=logged_in)

@socketio.on('send_message')
def handle_send_message(data):
    sender_id = session['user_id']
    receiver_id = data['receiver_id']
    content = data['message']
    
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()

    room = f"chat_{min(int(session['user_id']), int(data['receiver_id']))}_{max(int(session['user_id']), int(data['receiver_id']))}"

    emit('receive_message', {
        'sender': session['username'],
        'content': content
    }, room=room)

@socketio.on('join_room')
def handle_join_room(data):
    room = f"chat_{min(int(session['user_id']), int(data['receiver_id']))}_{max(int(session['user_id']), int(data['receiver_id']))}"

    join_room(room)
    
    emit('status', {'msg': 'Joined room: ' + room}, room=room)


@app.route('/users')
def users():

    logged_in = 'user_id' in session
    if not logged_in:
        return redirect(url_for('login'))  
    
    user = User.query.get(session['user_id'])
    
    search_query = request.args.get('search', '')
    if search_query:
        users = User.query.filter(
            User.username.contains(search_query),
            User.id != session['user_id']
        ).all()
    else:
        users = User.query.filter(User.id != session['user_id']).all()  
    
    skills = user.skills.split(",") if user.skills else []
    interests = user.interests.split(",") if user.interests else []

    return render_template(
        'users.html',
        user=user,
        skills=skills,
        interests=interests,
        logged_in=logged_in,
        users=users
    )


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000 )
