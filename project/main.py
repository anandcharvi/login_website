from flask import Blueprint, render_template
from flask_login import login_required, current_user
# from db import db
from .models import books

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name)

@main.route('/profile', methods=['POST'])
def profile_post():
    book_all = books.query.all()
    return render_template('book_menu.html', books_all=book_all)
    

@main.route('/staff_profile')
def staff_profile():
    return render_template('staff_profile.html')

# if __name__ == '__main__':
#     enter_data()
#     enter_books()
