from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sql.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(400), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.date}"

with app.app_context():
    db.create_all()

@app.route("/", methods = ['GET','POST'])
def hello_world():
    if(request.method == 'POST'):
        print("Post")
        t = request.form['title']
        d = request.form['desc']
        todo = Todo(title = t, desc = d)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)
    # return "<h1>Hello, World!</h1>"

@app.route("/show")
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return "<h1>This is Products Page</h1>"

@app.route("/delete/<int:sno>")
def delete(sno):
    q = Todo.query.filter_by(sno=sno).first()
    db.session.delete(q)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods = ['GET','POST'])
def update(sno):
    if(request.method == 'POST'):
        t = request.form['title']
        d = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.desc = d
        todo.title = t
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)

if(__name__ == "__main__"):
    app.run(debug=True, port=8000)