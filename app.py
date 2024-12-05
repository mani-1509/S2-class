from flask import Flask, render_template ,send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/test')
def test():
    return render_template('3Dtest.html')

@app.route('/static/<path:path>')
def static_proxy(path):
    # Ensure Flask sets the correct MIME type for .js files
    if path.endswith('.js'):
        return send_from_directory('static', path, mimetype='application/javascript')
    return send_from_directory('static', path)

@app.route('/node_modules/<path:path>')
def node_modules(path):
    return send_from_directory('node_modules', path)

if __name__ == "__main__":
    app.run(debug=True)
