"""Routes for user authentication."""
from flask import redirect, render_template, flash, request, url_for, abort
from flask import make_response
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from lynx.auth.forms import LoginForm, SignupForm, ForgotForm, ResetPasswordForm, ProfileForm, ChangePasswordForm, PreferencesForm, UserInfoForm
from lynx.auth.models import db, User
from lynx import login_manager
from lynx.auth import bpAuth
from lynx.services.mail_api import send_email
from datetime import date, timedelta
from lynx.services.token import confirm_token, generate_confirmation_token
from lynx.wallet.wallet import generateWallet
from lynx.auth.models import UserWallet
import datetime

@bpAuth.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # print(request.args.get('next'))
    login_form = LoginForm(request.form)
    # POST: Create user and redirect them to the app
    if request.method == 'POST':
        if login_form.validate() == False:    
            return render_template('auth/login.html',form=login_form)
        # Get Form Fields
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Validate Login Attempt
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user, remember=False) #, duration=timedelta(days=5))
                    next = request.args.get('next')
                    if user.email_confirmed != 'Y':
                        flash('Please verify your email address.')
                    
                    user.last_login = datetime.datetime.now()
                    db.session.commit()  

                    resp = make_response(redirect(next or url_for('home')))
                    if login_form.remember_me.data:
                        resp.set_cookie('usreml', email)
                    else:
                        resp.delete_cookie('usreml')           
                    return resp
                    #return redirect(next or url_for('home')) # SUCCESSFULL LOGIN
            flash('Invalid username or password')
        except Exception as e:
            app.logger.error(str(e), extra={'user': email})
            return redirect(url_for('errors.error'))
    # GET: Serve Log-in page
    em = request.cookies.get('usreml')
    if em is not None:
        login_form.email.data = em
        login_form.remember_me.data = True
    return render_template('auth/login.html',form=login_form)

def sendConfirmationEmail(email):
    token = generate_confirmation_token(email)
    text_body=render_template('auth/confirm_email.txt', token=token)
    send_email('LynX - Confirm Email Address', email, text_body,'')


@bpAuth.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign-up page."""
    signup_form = SignupForm(request.form)
    langs = []
    for lng in app.config['LANGUAGES'].items(): # items gives both: app.config['LANGUAGES'].keys() and .values()
        langs.append(lng)
    signup_form.language.choices = langs
    # POST: Sign user in
    if request.method == 'POST':
        if signup_form.validate():
            # Get Form Fields
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            email = request.form.get('email')
            password = request.form.get('password')
            phone = request.form.get('phone')
            language = request.form.get('language')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user is None:
                user = User(firstName=firstName,
                            lastName=lastName,
                            email=email,
                            password=generate_password_hash(password, method='sha256'),
                            phone=phone,
                            user_lang=language,
                            last_login = datetime.datetime.now(),
                            updatedBy=email,
                            email_confirmed='N',
                            userRole='U')
                db.session.add(user)
                db.session.flush() # populates new generated id
                key, address = generateWallet(user.id)
                wall = UserWallet(uid=user.id, mnemonic=str(user.id)+'xxx yyy zzz', privateKey=key, publicKey=str(user.id)+'pbkey', address=address, createdBy='lynx')
                db.session.add(wall) # save wallet to db
                
                sendConfirmationEmail(email)

                db.session.commit() # commit
                
                login_user(user)
                flash('Thank You. Please confirm email address using the link we sent to your email.')
                return redirect(url_for('home'))
            flash('A user already exists with that email address.')
            return redirect(url_for('auth.signup'))
    # GET: Serve Sign-up page
    return render_template('auth/signup.html',form=signup_form)

@bpAuth.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login', next=request.path))

@bpAuth.route("/forgot", methods=['GET', 'POST'])
def forgot():
    forgot_form = ForgotForm(request.form)
    linkSent = 'N'
    if request.method == 'POST':
        if forgot_form.validate():
            linkSent = 'Y' # tell user link is sent even if not a valid OR unregistered user email
            email = request.form.get('email')
            existing_user = User.query.filter_by(email=email).first()
            if not existing_user is None: #user exists, send reset link
                token = existing_user.get_reset_password_token()
                text_body=render_template('auth/reset_pwd_lnk.txt', user=existing_user, token=token)
                send_email('LynX - Reset Password', existing_user.email, text_body,'')
    return render_template('auth/forgot.html',form=forgot_form, linkSent=linkSent)


@bpAuth.route('/reset_pwd/<token>', methods=['GET', 'POST'])
def reset_pwd(token):
    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        user = User.verify_reset_password_token(token)
        if not user: #invalid token
            return redirect(url_for('home'))
        resetForm = ResetPasswordForm(request.form)

        if request.method == 'POST':
            if resetForm.validate():
                user.set_password(resetForm.password.data)
                db.session.commit()
                flash('Your password has been reset.')
                return redirect(url_for('home'))
        return render_template('auth/reset_pwd.html', form=resetForm)
    except Exception as e:
        app.logger.error(str(e), extra={'user': ''})
        return redirect(url_for('errors.error'))


@bpAuth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        abort(404)
    existing_user = User.query.filter_by(email=email).first_or_404()
    if not existing_user is None: #user exists
        existing_user.email_confirmed = 'Y'
        db.session.commit()
        flash('Your email has been confirmed.')
        return redirect(url_for('home'))


@bpAuth.route('/users')
def users():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    if current_user.userRole != "A":
        abort(401) # unauthorized

    allUsers = User.query.all()
    return render_template('auth/users.html', userList = allUsers)

@bpAuth.route('/profile', methods=['GET', 'POST'])
def profile():
    profile_form = ProfileForm(request.form)
    # POST: Sign user in
    if request.method == 'POST':
        if profile_form.validate():
            # Get Form Fields
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            phone = request.form.get('phone')
            userId = request.form.get('user_id')
            existing_user = User.query.filter_by(id=userId).first()
            if not existing_user is None:
                existing_user.firstName=firstName
                existing_user.lastName=lastName
                existing_user.phone=phone
                existing_user.updatedBy = current_user.email
                db.session.commit()
            flash('Profile successfully updated.')
            # return redirect(url_for('auth.profile', user_id = userId ))
            return redirect(url_for('home'))
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('home'))
        user_id = current_user.id

        user = User.query.filter_by(id=user_id).first()
        profile_form.firstName.data = user.firstName
        profile_form.lastName.data = user.lastName
        profile_form.phone.data = user.phone or ''
        profile_form.language.data = user.user_lang or ''
        profile_form.user_id.data = user.id

    return render_template('auth/profile.html',form=profile_form)

def validateStartDate(date_text):
    try:
        if datetime.datetime.strptime(date_text, '%m/%d/%Y'):
            return True
        else:
            return False
    except ValueError:
        pass

@bpAuth.route('/preferences', methods=['GET', 'POST'])
def preferences():
    pref_form = PreferencesForm(request.form)
    langs = []
    for lng in app.config['LANGUAGES'].items(): # items gives both: app.config['LANGUAGES'].keys() and .values()
        langs.append(lng)
    pref_form.language.choices = langs 
    if request.method == 'POST':
        if pref_form.validate():
            # Get Form Fields
            language = pref_form.language.data # request.form.get('language')
            userId = request.form.get('user_id')
            existing_user = User.query.filter_by(id=userId).first()
            if not existing_user is None:
                existing_user.user_lang=language
                existing_user.updatedBy = current_user.email
                db.session.commit()
            flash('Preferences successfully updated.')
            # return redirect(url_for('auth.profile', user_id = userId ))
            return redirect(url_for('home'))
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('home'))
        else: 
            user_id = current_user.id

        user = User.query.filter_by(id=user_id).first()

        pref_form.language.data = user.user_lang or 'en'
        pref_form.user_id.data = user.id

    return render_template('auth/preferences.html',form=pref_form)

@bpAuth.route('/security', methods=['GET', 'POST'])
def security():
    changePwd_form = ChangePasswordForm(request.form)
    if request.method == 'POST':
        if changePwd_form.validate():
            if current_user.check_password(password=changePwd_form.currentpassword.data):
                if not current_user is None:
                    current_user.set_password(changePwd_form.password.data)
                    db.session.commit()
                    flash('Your password has been changed.')
                    return redirect(url_for('home'))
            flash('Incorrent current password.')
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('home'))

    return render_template('auth/security.html',form=changePwd_form)

@bpAuth.route('/userinfo/<user_id>', methods=['GET', 'POST'])
def userinfo(user_id = 0):
    user_form = UserInfoForm(request.form)
    if request.method == 'POST':
        if current_user.userRole != "A":
            abort(401) # unauthorized
        if user_form.validate():
            # Get Form Fields
            # firstName = request.form.get('firstName')
            # lastName = request.form.get('lastName')
            # userId = request.form.get('user_id')
            # existing_user = User.query.filter_by(id=userId).first()
            # if not existing_user is None:
            #     existing_user.firstName=firstName
            #     existing_user.lastName=lastName
            #     existing_user.updatedBy = current_user.email
            #     db.session.commit()

            # wall = genwall(userId)
            # saveWall(wall)

            flash('Profile successfully updated') #: ' + wall.address)
            return redirect(url_for('home'))
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('home'))
        if current_user.userRole != "A":
            abort(401) # unauthorized

        user = User.query.filter_by(id=user_id).first()
        user_form.firstName.data = user.firstName
        user_form.lastName.data = user.lastName
        user_form.user_id.data = user.id

    return render_template('auth/userinfo.html',form=user_form)