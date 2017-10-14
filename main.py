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
        entry_title = request.form['title']
        entry_date = request.form['date']
        entry_content = request.form['content']

        if len(entry_title) < 1 or len(entry_content) < 1:
            flash("Title and content are required!")
            return redirect('/addnew')

        entry = Blog(entry_title, entry_date, entry_content)
        db.session.add(entry)
        db.session.commit()

        return render_template('blog_entry.html', title="Blog Entry", entry=entry)
        
    else:
        return render_template('addnew.html')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    entry_id = request.args.get('id')
    
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('blog_entry.html', title="Blog Entry", entry=entry)

    else:
        blogs = Blog.query.all()
    return render_template('blog.html', title="Blog Posts", blogs=blogs)
if __name__ == '__main__':
    app.run()