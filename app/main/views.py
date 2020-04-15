from flask import render_template, session, redirect, url_for, flash
from . import main
from .forms import newGameForm, joinGameForm
from .. import db
from ..models import Game, User, Role
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required

@main.route('/')
def index():
	return render_template('login.html')

@main.route('/start')
@login_required
def start():
	return render_template('index.html')

@main.route('/admin')
@login_required
@admin_required
def forAdmin():
	return '<h1>For ADMIN!!</h1>'

@main.route('/viewGameDetails/<game_id>',methods=['GET'])
@login_required
def viewGameInfo(game_id):
	game = Game.query.filter_by(id=game_id).all()
	if game:
		print(game)
	else:
		print('no game with that id')
	return '<h1>viewing Game Information</h1>'

@main.route('/createGame', methods=['GET','POST'])
@login_required
def createGame():
	form = newGameForm()
	if form.validate_on_submit():
		if current_user.game_id is None:
			game = Game(rules=form.rules.data)
			current_user.role = Role.query.filter_by(name='Administrator').first()
			current_user.game_id = game.id
			print(current_user.role)
			db.session.add(game)
			db.session.commit()
			return redirect('/')
		else:
			flash('You are already in a game')
	return render_template('createGame.html', form=form)
	
@main.route('/joinGame', methods=['GET','POST'])
@login_required
def joinGame():
	form = joinGameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=session['username']).first()
		game = Game.query.filter_by(id=form.code.data)
		if user and game:	
			if user.game_id is None:
				user.game_id = form.code.data	
				db.session.commit()
			else:
				flash('You are already in a game')
	return render_template('joinGame.html', form=form)
