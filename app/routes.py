from flask import render_template, jsonify,request,redirect,url_for,session,flash
from app import app, db
from app.forms import RegistrationForm, LoginForm, DataForm,DepositForm, WithdrawForm
from app.models import User, AccountDetails
from flask_login import login_required , login_user,logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
print(app)

@app.route('/',methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    print("home called")
    return render_template("home.html")

@app.route('/register',methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        id=form.id.data
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password).decode('utf-8')

        email = form.email.data
        new_user = User(id=id, username=username, password=hashed_password, email=email)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})

    return render_template("register.html",form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Assuming LoginForm is properly defined

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Successful login
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login

        # Incorrect username or password
        error = 'Invalid username or password'
        return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



from flask_login import current_user

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        user_id = current_user.id  # Retrieve the current user's ID from Flask-Login
        print(user_id)
        account_details = AccountDetails.query.filter_by(user_id=user_id).all()
        if not account_details:
            flash('No account details found for the current user.')
        return render_template('dashboard.html', account_details=account_details)
    else:
        return redirect(url_for('login'))  # Redirect to the register route if the user is not logged in


@app.route('/registerdata',methods=['GET','POST'])
def registerdata():
    form= DataForm()
    if form.validate_on_submit():
        id=form.id.data
        name=form.name.data
        account_number=form.account_number.data
        balance=form.balance.data
        user_id=form.user_id.data

        new_accounts = AccountDetails(id=id, name=name, account_number= account_number,balance=balance,user_id=user_id)
        print(new_accounts)
        db.session.add(new_accounts)
        db.session.commit()
        return jsonify({'message': 'Account registered successfully'})

    return render_template("registerdata.html",form=form)

@app.route('/Deposit',methods=['GET','POST'])
@login_required
def Deposit():
    form= DepositForm()
    account=None
    if current_user.is_authenticated:
        user_id = current_user.id  # Retrieve the current user's ID from Flask-Login
        account = AccountDetails.query.filter_by(user_id=user_id).first()
    if form.validate_on_submit():
        new_bal=form.amount.data
        if account:
            # Update the balance by adding the deposit amount
            account.balance += new_bal
            # Commit the changes to the database
            db.session.commit()
            return redirect(url_for('dashboard'))  # Redirect to dashboard or another page after deposit
        else:
            return "Account not found"
    else:
        return render_template('Deposit.html',form=form,account=account)

@app.route('/Withdraw',methods=['GET','POST'])
@login_required
def Withdraw():
    form= WithdrawForm()
    account=None
    if current_user.is_authenticated:
        user_id = current_user.id  # Retrieve the current user's ID from Flask-Login
        account = AccountDetails.query.filter_by(user_id=user_id).first()
    if form.validate_on_submit():
        new_bal=form.amount.data
        if account:
            # Update the balance by adding the deposit amount
            if account.balance> new_bal:
                account.balance -= new_bal
            # Commit the changes to the database
                db.session.commit()
                return redirect(url_for('dashboard'))  # Redirect to dashboard or another page after deposit
            else:
                return "low Balance"
        else:
            return "Account not found"
    else:
        return render_template('Withdrawal.html',form=form,account=account)