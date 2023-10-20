from app import create_app, db
from app.Model.models import Review, User, Book, Year

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'Review': Review, 'User': User}

@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()
        if Book.query.count() == 0:
            books = [{'title':'Percy Jackson and the Olympians', 'author':'Rick Riordan'},
                    {'title':'Emma', 'author':'Jane Austen'},
                    {'title':'Vicious', 'author':'VE Schwab'},
                    ]
            for t in books:
                db.session.add(Book(title=t['title'],author=t['author']))
                
        if Year.query.count() == 0:
            for i in range(2023, 1949, -1):
                db.session.add(Year(year=i))

            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)