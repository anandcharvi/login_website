from .models import books, User
from . import db

def enter_books():
    book_info = (
            (1234, "Don Quixote", 5),
            (1235, "Lord of the Rings", 3),
            (1236, "Harry Potter", 2),
            (1237, "Alice's Adventures in Wonderland", 1),
            (1238, "And Then There Were None", 3),
            (1239, "The Lion, the Witch, and the Wardrobe", 4),
            (1230, "Pinocchio", 10),
            (1231, "Catcher in the Rye", 5),
            (1232, "Fault In our Stars", 7),
            (1233, "Anne Of Green Gables", 6),
        )

    for i in book_info:
        new_book = books(book_id=i[0], book_name=i[1], Inventory=i[2])
        db.session.add(new_book)

    db.session.commit()
    
def user_info():
    user_info = (
        (9234, "Emily", "Emily@gmail", "Em01"),
        (9235, "Gabriel", "Gabriel@gmail", "Ga01"),
        (9236, "Cammillie","Cammillie@gmail", "Ca01"),
        (9237, "Raquel","Raquel@gmail", "Ra01"),
        (9238, "Sergio", "Sergio@gmail","Se01"),
        (9239, "Mindy", "Mindy@gmail","Mi01"),
        (9230, "George", "George@gmail","Ge01"),
        (9231, "Bob", "Bob@gmail","Bo01"),
        (9232, "Noddy", "Noddy@gmail","No01"),
        (9233, "Oswald", "Oswald@gmail","Os01"),
    )
    for i in user_info:
        new_user = User(id=i[0], name=i[1], email=i[2], password = i[3])
        db.session.add(new_user)

    db.session.commit()

# if __name__ == '__main__':
#     enter_books()
#     user_info()
