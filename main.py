from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'r44uifgstt8o'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date = db.Column(db.String(10))
    content = db.Column(db.String(50000))

    def __init__(self, title, date, content):
        self.title = title
        self.date = date
        self.content = content
    
    def __repr__(self):
        return '<Blog %r>' % self.title, self.date, self.content

@app.route('/', methods=['POST', 'GET'])
def index():
    # TODO Add login
    return render_template('index.html',title="Build-a-Blog")

@app.route('/addnew', methods=['POST', 'GET'])
def addnew():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_date = request.form['date']
        blog_content = request.form['content']
        blog = Blog(blog_title, blog_date, blog_content)

        if len(blog_title) < 1 or len(blog_content) < 1:
            flash("Title and content are required!")
            return redirect('/addnew')

        db.session.add(blog)
        db.session.commit()
        return redirect('/blog')

    else:
        return render_template('addnew.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():    
    blogs = Blog.query.all()
    return render_template('blog.html',title="Blog Posts", 
        blogs=blogs)

if __name__ == '__main__':
    app.run()