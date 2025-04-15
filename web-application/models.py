from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<User {self.username}>"

class Book(db.Model):
    __tablename__ = 'books'
    
    book_id = db.Column('Book ID', db.String(20), primary_key=True)
    title = db.Column('Title', db.String(255), nullable=False)
    author = db.Column('Author', db.String(100), nullable=False)
    genre = db.Column('Genre', db.String(50), nullable=False)
    publication_year = db.Column('Publication Year', db.Integer)
    copies_available = db.Column('Copies Available', db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<Book {self.title}>"

class Member(db.Model):
    __tablename__ = 'members'
    
    id_number = db.Column('ID Number', db.String(10), index=True)
    membership_number = db.Column('Membership Number', db.String(10), primary_key=True)
    name = db.Column('Name', db.String(100), nullable=False)
    contact_info = db.Column('Contact Info', db.String(20))
    membership_type = db.Column('Membership Type', db.String(20), nullable=False)
    join_date = db.Column('Join Date', db.String(20), nullable=False)  # Changed to String
    expiration_date = db.Column('Expiration Date', db.String(20), nullable=False)  # Changed to String
    
    def __repr__(self):
        return f"<Member {self.name}>"

class Loan(db.Model):
    __tablename__ = 'loans'
    
    loan_number = db.Column('Loan Number', db.String(10), primary_key=True)
    book_id = db.Column('Book ID', db.String(20), db.ForeignKey('books.Book ID'), nullable=False)
    member_id = db.Column('Member ID', db.String(10), db.ForeignKey('members.Membership Number'), nullable=False)
    loan_date = db.Column('Loan Date', db.String(20), nullable=False)  # Changed to String
    due_date = db.Column('Due Date', db.String(20), nullable=False)  # Changed to String
    return_date = db.Column('Return Date', db.String(20), nullable=True)  # Changed to String
    
    # Relationships
    book = db.relationship('Book', backref='loans')
    member = db.relationship('Member', backref='loans')
    
    def __repr__(self):
        return f"<Loan {self.loan_number}>"