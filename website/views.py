from sys import flags
from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_required, current_user
from . import db
import re
import random
from .models import Puzzle


views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # items = Item.query.all()

    # if request.method == 'POST':
    #     search = request.form.get('search')
    #     print(search)
    #     items = Item.query.filter_by(name=search).all()
    #     if len(items) < 1:
    #         flash(f'No results found by the name of {search}', category='alert')

    return render_template("home.html", user=current_user)

@views.route('/puzzles', methods=['GET', 'POST'])
@login_required
def puzzles():
    
    seen_puzzles = []
    
    length = Puzzle.query.count()
    print(length)
    def randid():
        if length != 1:
            id = random.randrange(1, length+1, 1)
        else:
            id = 1
        return id
    
    id = randid()

    puzzle = Puzzle.query.filter_by(id=int(id)).first()
    
    # puzzle = Puzzle.query.first()
    
    if request.method == 'POST':
        guess = request.form.get('guess')
        answer = puzzle.answer
        
        compare = re.search(answer.lower(), guess.lower())
        
        if guess == '':
            flash("Please submit an answer", category='error')
        elif compare:
            flash('Correct!', category='success')
            seen_puzzles.append(puzzle.id)
            
            new_id = randid()
            
            puzzle = Puzzle.query.filter_by(id=int(new_id)).first()
            
            answer = puzzle.answer
            
        else:
            flash("Try again", category='alert')
         
    return render_template("puzzles.html", user=current_user, puzzle=puzzle)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        difficulty = request.form.get('difficulty')
        
        new_puzzle = Puzzle(question=question, answer=answer, difficulty=int(difficulty))
        db.session.add(new_puzzle)
        db.session.commit()
        flash('Puzzle added!', category='success')

    puzzles = Puzzle.query.all()
    return render_template("admin.html", user=current_user, puzzles=puzzles)