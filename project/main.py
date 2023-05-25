from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import books, books_record, User
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)


@main.route('/')
def index():
    user = User.query.filter_by(email="library_staff@library.in").first()
    if user:
        return render_template('index.html')
    else:
        staff_password = "staff123#"
        new_user = User(email="library_staff@library.in", name="staff", password=generate_password_hash(staff_password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return render_template('index.html')

@main.route('/<int:user_id>/profile')
# @main.route('/profile')
@login_required
def profile(user_id):
    book_list = due_books(user_id)
    # print(book_list)
    if book_list is None:
        book_list = []
    return render_template('profile.html', name=current_user.name, book_list = book_list)
    # return render_template('profile.html',name=current_user.name)


def due_books(id):
    book_id_list=[]
    book_list=[]
    record = books_record.query.filter_by(user_id = id).all()
    if len(record)>0:
     for r in record:
         if r.status == "Issued" or r.status == "issued":
             book_id_list.append(r.book_id)
     book_list = list(map(book_name,book_id_list))
     return book_list

def book_name(id):
    book = books.query.filter_by(book_id = id).all()
    for b in book:
        return b.book_name
    
@main.route('/profile', methods=['POST'])
def profile_post():
    book_all = books.query.all()
    # TO DO Logic to remove issued books by the user from all books
    return render_template('book_menu.html', books_all=book_all)
    

@main.route('/staff_profile')
@login_required
def staff_profile():
    return render_template('staff_profile.html')

# if __name__ == '__main__':
#     enter_data()
#     enter_books()
