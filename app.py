from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
db = SQLAlchemy(app)

# Admin credentials (plain text)
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "Test@12345"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            new_question = Question(question_text=question)
            db.session.add(new_question)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Username: {username}, Password: {password}")  # Debug statement
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('admin_login.html')

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    questions = Question.query.all() # Fetch all questions from the database
    return render_template('admin_panel.html', questions=questions)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Flask application is starting...")  # Debug statement
    app.run(host='0.0.0.0', port=5000, debug=True)  # Bind to all network interfaces