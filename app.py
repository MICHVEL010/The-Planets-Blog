#Editor : Michael Raouf Eldeeb
#Editor : Heba Elsayed
#----------------------------------------------------------------


from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
import sqlite3

app = Flask(__name__ , static_url_path='/static')
app.config['SECRET_KEY'] = 'your_secret_key'
db_file = 'users.db'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
principals = Principal(app)

with app.app_context():
    conn = sqlite3.connect(db_file)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.execute("CREATE TABLE IF NOT EXISTS feedback(fristName, lastName, email, URL, Subject, Comments)")
    conn.commit()
    conn.close()

class User(UserMixin):
    def init(self, id, username):
        self.id = id
        self.username = username

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
class FeedBackForm(FlaskForm):
    firstName = StringField('firstName', validators=[DataRequired()])
    lastName = StringField('lastName', validators=[DataRequired()])
    email = PasswordField('email', validators=[DataRequired()])
    URL = PasswordField('URL', validators=[DataRequired()])
    Subject = PasswordField('Subject', validators=[DataRequired()])
    Comments = PasswordField('Comments', validators=[DataRequired()])
    submit = SubmitField('Submit FeedBack')
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        id, username, password = user_data
        return User(id, username)
    return None

@app.route('/')
@login_required
def home():
    return render_template('Home.html')

@app.route('/Home')
def Home():
   return render_template('Home.html')

@app.route('/Earth')
def Earth():
   return render_template('Earth.html')

@app.route('/Moon')
def Moon():
   return render_template('Moon.html')

@app.route('/Mars')
def Mars():
   return render_template('Mars.html')

@app.route('/Mercury')
def Mercury():
   return render_template('Mercury.html')

@app.route('/Sun')
def Sun():
   return render_template('Sun.html')

@app.route('/venus')
def venus():
   return render_template('venus.html')

@app.route('/AboutUs')
def about():
    return render_template('AboutUs.html')

@app.route('/Bibliography')
def Bibliography():
    return render_template('Bibliography.html')

@app.route('/FeedBack')
def FeedBack():
    return render_template('FeedBack.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        
        if user_data and user_data[2] == password:
            # user = User(user_data[0], user_data[1])
            # login_user(user)
            # flash('Login successful!', 'success')
            # return redirect(url_for('dashboard'))
            return render_template('Home.html')
        else:
            flash('Login failed. Please check your username and password.', 'danger')
        
        conn.close()
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()

            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))

        
    
    return render_template('signup.html', form=form)

@app.route('/FeedBack', methods=['GET', 'POST'])
def feedback():
    form = FeedBackForm()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        URL = form.URL.data
        Subject = form.Subject.data
        Comments = form.Comments.data

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO users (firstName, lastName, email, URL, Subject, Comments) VALUES (?, ?, ?, ?, ?, ?)', (firstName, lastName, email, URL, Subject, Comments))
        conn.commit()
        conn.close()
        res = conn.execute("SELECT * FROM feedback")
        res.fetchall()
        flash('Thank you for your FeedBack', 'success')
        return redirect(url_for('FeedBack'))

        
    
    return render_template('FeedBack.html', form=form)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)