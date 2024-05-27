from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from forms import AddPup, DelPup, AddOwner
from main import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Puppies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    owner = db.relationship('Owners', backref='puppy', cascade='all, delete', uselist=False)

    def __init__(self, breed, age) -> None:
        super().__init__()
        self.breed = breed
        self.age = age
    
    def __repr__(self) -> str:
        return f"id: {self.id} breed: {self.breed} age: {self.age} owner: {self.owner}"


class Owners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, puppy_id, name) -> None:
        super().__init__()
        self.name = name
        self.puppy_id = puppy_id
    
    def __repr__(self) -> str:
        return f"name: {self.name} puppy_id: {self.puppy_id} id: {self.id}"


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/add_pup', methods=['GET', 'POST'])
def add_pup():
    form = AddPup()

    if form.validate_on_submit():
        new_pup = Puppies(form.breed.data, form.age.data)
        db.session.add(new_pup)
        db.session.commit()
        return redirect(url_for('view_pups'))

    return render_template('add_pup.html', form=form)

@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    form = AddOwner()

    if form.validate_on_submit():
        new_owner = Owners(form.puppy_id.data, form.name.data)
        db.session.add(new_owner)
        db.session.commit()
        flash(f'Added new owner: {form.name.data}')
        return redirect(url_for('view_pups'))
    
    return render_template('add_owner.html', form=form)

@app.route('/del_pup', methods=['GET', 'POST'])
def del_pup():
    form = DelPup()

    if form.validate_on_submit():
        pup = db.session.get(Puppies, form.id.data)
        db.session.delete(pup)
        db.session.commit()
        return redirect(url_for('view_pups'))

    return render_template('del_pup.html', form=form)

@app.route('/view_pups')
def view_pups():
    pups = Puppies.query.all()
    return render_template('view_pups.html', pups=pups)


if __name__ == '__main__':
    app.run(debug=True)
