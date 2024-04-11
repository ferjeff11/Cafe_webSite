from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    wifi = db.Column(db.Boolean, nullable=False)
    coffee = db.Column(db.Boolean, nullable=False)

@app.route('/')
def index():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        wifi = 'wifi' in request.form
        coffee = 'coffee' in request.form
        new_cafe = Cafe(name=name, location=location, wifi=wifi, coffee=coffee)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_cafe.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_cafe(id):
    cafe_to_delete = Cafe.query.get_or_404(id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
