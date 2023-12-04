from app import create_app, db
from app.Model.models import Review, User, Book, Year, Genre

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'Review': Review, 'User': User}

@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()
        if Book.query.count() == 0:
            books = [{'title':'Percy Jackson and the Olympians', 'author':'Rick Riordan', 'cover':'covers/book1.png'},
                    {'title':'Emma', 'author':'Jane Austen', 'cover':'covers/book2.png'},
                    {'title':'Vicious', 'author':'VE Schwab', 'cover':'covers/book3.png'},
                    ]
            for t in books:
                db.session.add(Book(title=t['title'],author=t['author'], cover=t['cover']))
                db.session.commit()
                
        if Year.query.count() == 0:
            for i in range(2023, 1949, -1):
                db.session.add(Year(year=i))

            db.session.commit()

        if Genre.query.count() == 0:
            genres = ['Fiction','Non-Fiction', 'Mystery', 'Romance', 'Fantasy']
            for g in genres:
                db.session.add(Genre(name=g))
            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)