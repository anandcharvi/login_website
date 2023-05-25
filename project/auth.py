from flask import Blueprint, render_template,redirect,url_for,request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, books, books_record
from . import db
from flask_login import login_user,login_required, current_user, logout_user
from .enter_data import *
import datetime
from sqlalchemy import func, and_

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect Credentials! Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    else:
        flash('Logged in successfully!', category='success')
        login_user(user, remember=remember)
        # return redirect(url_for('main.profile'))
        return redirect(url_for('main.profile', user_id = user.id))

    

@auth.route('/staff_login')
def staff_login():
    return render_template('staff_login.html')

@auth.route('/staff_login', methods=['POST'])
def staff_login_post():
    password = request.form.get('password')
    # password=generate_password_hash(password, method='sha256')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email="library_staff@library.in").first()

    if user and check_password_hash(user.password, password):
        login_user(user, remember=remember)
        return redirect(url_for('main.staff_profile'))
     
    else:
        flash('Incorrect Password! Please try again.')
        return redirect(url_for('auth.staff_login'))
        

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    else:
        
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash('Registration completed!', category='success')
        return redirect(url_for('auth.login'))
    
@auth.route('/add_book', methods=['POST'])
def add_book():
    btn = request.form.get("response")
    if btn == "add":
        return render_template('add_book.html')
    elif btn == "update_book":
        books_all = books.query.all()
        return render_template('update_book.html', books_all=books_all)
    elif btn == "update_user":
        user_all = User.query.all()
        return render_template('update_user.html', user_all=user_all)
    elif btn == "bulk_books":
        count = enter_books()
        flash(count + " books added to database")
        return redirect(url_for('main.staff_profile'))
    elif btn == "bulk_users":
        count = enter_user()
        flash(count + " users added to database")
        return redirect(url_for('main.staff_profile'))
    elif btn == "records":
        records = books_record.query.all()
        return render_template('records.html', records=records)
    

@auth.route('/add_book_post', methods=['POST'])
def add_book_post():
    book_id = request.form.get('book_id')
    book_name = request.form.get('book_name')
    inventory = request.form.get('inventory')

    book = books.query.filter_by(book_id=book_id).first() # if this returns a user, then the email already exists in database

    if book: # if a book is found, we want to redirect back .
        flash('book already exists. Please update inventory')
        return redirect(url_for('auth.add_book'))
    
    else:
        
        new_book = books(book_id=book_id, book_name=book_name, Inventory=inventory)
       
        db.session.add(new_book)
        db.session.commit()
        flash('book added successfully', category='success')
        return redirect(url_for('main.staff_profile'))
    # return render_template('add_book.html')
    
@auth.route('/<int:book_id>/issue')
# @login_required
def issue(book_id):
    book = books.query.get(book_id)
    book.Inventory=book.Inventory-1
    # print(book.Inventory)
    max_ref_no = db.session.query(func.max(books_record.ref_id)).scalar()
    ref_no = max_ref_no + 1
    new_record = books_record(ref_id=ref_no, user_id = current_user.id, book_id = book_id, status = "Issued", issue_date=datetime.date.today(), return_date = None)

    # add the new user to the database
    db.session.add(new_record)
    db.session.commit()
    flash(book.book_name + ' issued successfully. You need to return this book within 30 days....\nYour reference number is ' + str(ref_no), category='success')
    return redirect(url_for('main.profile', user_id = current_user.id,))

@auth.route('/<string:book_name>/return_book')
# @login_required
def return_book(book_name):
    book = books.query.filter_by(book_name=book_name).first()
    book.Inventory=book.Inventory+1
    print(book.Inventory)
    book_ref_no = books_record.query.filter_by(book_id=book.book_id, user_id=current_user.id, status = "Issued").first()
    ref_no = book_ref_no.ref_id
    # ref_no = str(book.book_id) + str(current_user.id)
    record = books_record.query.get(ref_no)
    record.status = "Returned"
    record.return_date = datetime.date.today()
    db.session.commit()
    flash(book_name + ' returned successfully. ', category='success')
    return redirect(url_for('main.profile',user_id = current_user.id))

@auth.route('/<int:book_id>/remove')
# @login_required
def remove(book_id):
    book = books.query.get_or_404(book_id)
    book_name = book.book_name
    db.session.delete(book)
    db.session.commit()
    books_all = books.query.all()
    flash(book_name + 'removed successfully', category='success')
    return render_template('update_book.html', books_all=books_all)
    # return redirect(url_for('main.staff_profile'))

@auth.route('/<int:id>/remove_user')
# @login_required
def remove_user(id):
    user = User.query.get_or_404(id)
    name = User.name
    db.session.delete(user)
    db.session.commit()
    user_all = books.query.all()
    flash(name + 'removed successfully', category='success')
    return render_template('update_user.html', user_all=user_all)



@auth.route('/<int:book_id>/edit/', methods=('GET', 'POST'))
def edit(book_id):
    book = books.query.get(book_id)

    if request.method == 'POST':
        book_name = request.form['book_name']
        Inventory = int(request.form['Inventory'])

        book.book_id = book_id
        book.book_name = book_name
        book.Inventory = Inventory
        
        db.session.add(book)
        db.session.commit()

        flash(book_name + ' is updated successfully', category='success')
        
        books_all = books.query.all()
        return render_template('update_book.html', books_all=books_all)

    return render_template('edit.html', book=book)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    # return render_template('logout.html', name = current_user.name)
