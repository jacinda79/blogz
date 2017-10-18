from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'r44uifgstt8o'

def username_val(username):
    username_error = ""
    if len(username) not in range(3, 21):
        username_error = 'Username must be between 3 and 20 characters.'
    if ' ' in username:
        username_error = "Username can't contain spaces."
    return username_error

def pass_val(password, verify):
    pass_error = ""
    if password != verify:
        pass_error = "Passwords don't match."
    if len(password) not in range(3, 21):
        pass_error = 'Passwords must be between 3 and 20 characters.'
    return pass_error

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date = db.Column(db.String(10))
    content = db.Column(db.String(50000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, date, content, owner):
        self.title = title
        self.date = date
        self.content = content
        self.owner_id = owner

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return str(self.username)
    
    #def __repr__(self):
    #    return '<Blog %r>' % self.title, self.date, self.content

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index', 'static']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = username
            flash("Logged in")
            return redirect('/addnew')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            return redirect('/login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_error = username_val(username)
        pass_error = pass_val(password, verify)
        existing_user = User.query.filter_by(username=username).first()
        if not all(x is "" for x in (username_error, pass_error)):
            if username_error:
                flash(username_error)
            if pass_error:
                flash(pass_error)
            return redirect('/signup')
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            return redirect('/addnew')
        else:
            flash('User already exists')
            return redirect('/signup')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html',title="Blogz")

@app.route('/addnew', methods=['POST', 'GET'])
def addnew():
    owner_id = User.query.filter_by(username=session['user']).first()
    if request.method == 'GET':
        return render_template('addnew.html')
    else:
        entry_title = request.form['title']
        entry_date = request.form['date']
        entry_content = request.form['content']
        if not entry_title or not entry_content:
            flash("Title and content are required!")
            return redirect('/addnew')
        else:
            entry = Blog(entry_title, entry_date, entry_content, owner_id)
            db.session.add(entry)
            db.session.commit()
            return redirect('/blog_entry')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    entry_id = request.args.get('id')
    
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('blog_entry.html', title="Blog Entry", entry=entry)
    else:
        blogs = Blog.query.all()
    return render_template('blog.html', title="Blog Posts", blogs=blogs)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['user']
    return redirect('/')

if __name__ == '__main__':
    app.run()