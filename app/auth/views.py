from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from app import db
from app.models import User
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.token import gen_token, verify_token
from app.utils.email import send_email

auth = Blueprint('auth', __name__)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # If user is logged in, redirect
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit(): # For valid post request
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = gen_token(user.email)
        send_email(
            to=user.email, subject='Confirm Your Account',
            template='auth/email/confirm', user=user, token=token
        )

        login_user(user)

        flash('A confirmation email has been sent.', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', title="Register", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm_email(token):
    try:
        email = verify_token(token)

        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash('Account is already confirmed. Please login.', 'success')
        else:
            user.confirmed = True

            db.session.add(user)
            db.session.commit()
            flash('You have been confirmed. Thanks!', 'success')
            return redirect(url_for('main.index'))
    except:
        flash('The confirmation link is invalid or has expired', 'danger')
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = gen_token(current_user.email)
    send_email(to=current_user.email, subject='Confirm Your Account',
               template='auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
    return render_template('auth/login.html', title="Login", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))
