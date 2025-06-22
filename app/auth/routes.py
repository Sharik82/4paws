from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

# Вхід
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Невірні дані для входу.')
            return redirect(url_for('auth.login'))

        # тільки user_id
        session['user_id'] = user.id
        session.permanent = True

        if user.is_admin:
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('cabinet.profile'))

    return render_template('cabinet/login.html')


# Реєстрація
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Користувач вже існує. Увійдіть у кабінет.')
            return redirect(url_for('auth.login'))

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        # тільки user_id
        session['user_id'] = user.id
        session.permanent = True

        flash('Успішна реєстрація!')
        return redirect(url_for('cabinet.profile'))

    return render_template('cabinet/register.html')


# Вихід
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Ви вийшли з акаунту.')
    return redirect(url_for('auth.register'))
