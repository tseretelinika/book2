from ext import app, db
from flask import render_template, redirect, flash
from forms import RegisterForm, BookForm, LoginForm
from models import Book, Review, User
from flask_login import login_user, logout_user, login_required
from os import path

profiles = []


@app.route("/")
def home():
    books = Book.query.all()
    # books =Book.query.filter(Book.title == "little prince").all()
    return render_template("index.html", books=books, role="admin")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/book/<int:book_id>")
def view_book(book_id):
    book = db.session.get(Book, book_id)
    reviews = Review.query.filter(Review.book_id == book_id).all()
    if book:
        return render_template("book_details.html", book=book, reviews=reviews)
    return "Book Not Found"

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
        )
        img = form.image.data
        if img:
            directory = path.join(app.root_path, "static", "images", img.filename)
            img.save(directory)
            new_book.image = img.filename
        new_book.create()
        return redirect("/")
    return render_template("add_book.html", form=form)


@app.route("/update_book/<int:book_id>", methods=["GET", "POST"])
@login_required
def update_book(book_id):
    book = db.session.get(Book, book_id)
    form = BookForm(title=book.title, author=book.author)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        image = form.image.data
        if image:
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            book.image = image.filename
        book.save()
        return redirect("/")
    return render_template("add_book.html", form=form)


@app.route("/delete_book/<int:book_id>")
@login_required
def delete_book(book_id):
    book = db.session.get(Book, book_id)
    book.delete()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("წარმატებით შეხვედი საიტზე, ყოჩაღ ძმაო!")
            return redirect("/")
        flash("Invalid username or password")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        password=form.password.data)
        new_user.create()
        flash("წარმატებით დარეგისტრირდი")
        return redirect("/")
    return render_template("register.html", form=form)



