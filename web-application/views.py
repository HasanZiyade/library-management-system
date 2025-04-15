from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Book, Member, Loan
from datetime import datetime, date, timedelta
from sqlalchemy import func, desc

main_bp = Blueprint('main', __name__)

# Helper function to convert string dates to datetime objects
def parse_date(date_str):
    if date_str is None:
        return None
    
    # Check if already a date/datetime object
    if isinstance(date_str, (datetime, date)):
        return date_str
        
    # Try different date formats
    formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except (ValueError, TypeError):
            continue
    
    # If all formats fail, return the original string
    print(f"Warning: Could not parse date string: {date_str}")
    return date_str

@main_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        # Get current date for comparisons
        today = datetime.now().date()
        
        # Get counts from database
        book_count = db.session.query(Book).count()
        member_count = db.session.query(Member).count()
        
        # Active loans = loans that haven't been returned
        active_loans = db.session.query(Loan).filter(Loan.return_date == None).count()
        
        # Overdue loans = loans past due date that haven't been returned
        overdue_loans = db.session.query(Loan).filter(
            Loan.due_date < today,
            Loan.return_date == None
        ).count()
        
        # Get recent loans (last 5)
        recent_loans_raw = db.session.query(Loan).order_by(desc(Loan.loan_date)).limit(5).all()
        
        # Process the loan data to ensure dates are proper datetime objects
        recent_loans = []
        for loan in recent_loans_raw:
            # Create a new dictionary with processed dates
            processed_loan = {
                'loan_number': loan.loan_number,
                'book_id': loan.book_id,
                'member_id': loan.member_id,
                'loan_date': parse_date(loan.loan_date),
                'due_date': parse_date(loan.due_date),
                'return_date': parse_date(loan.return_date) if loan.return_date else None,
            }
            recent_loans.append(processed_loan)
        
        # Get recent activities
        recent_activities = []
        
        # Recent loans
        for loan in recent_loans:
            # Get the book and member details for this loan
            book = db.session.query(Book).filter(Book.book_id == loan['book_id']).first()
            member = db.session.query(Member).filter(Member.membership_number == loan['member_id']).first()
            
            if book and member:
                activity_type = "borrow" if loan['return_date'] is None else "return"
                activity = {
                    'type': activity_type,
                    'book_title': book.title,
                    'member_name': member.name,
                    'date': loan['loan_date'] if activity_type == "borrow" else loan['return_date'],
                    'loan_number': loan['loan_number']
                }
                recent_activities.append(activity)
        
        # Get popular books (most loaned)
        popular_books_query = db.session.query(
            Book, 
            func.count(Loan.book_id).label('loan_count')
        ).join(Loan, Book.book_id == Loan.book_id)\
         .group_by(Book.book_id)\
         .order_by(desc('loan_count'))\
         .limit(4)
        
        popular_books = popular_books_query.all()
        
        return render_template('dashboard.html', 
                            username=current_user.username,
                            book_count=book_count,
                            member_count=member_count,
                            active_loans=active_loans,
                            overdue_loans=overdue_loans,
                            recent_activities=recent_activities,
                            popular_books=popular_books,
                            recent_loans=recent_loans,
                            today=today)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Dashboard error: {str(e)}")
        print(f"Error details: {error_details}")
        return render_template('dashboard.html', 
                            username=current_user.username,
                            error=str(e),
                            error_details=error_details)

@main_bp.route('/books')
@login_required
def books():
    try:
        # Get filter values from query string
        genre = request.args.get('genre', '')
        availability = request.args.get('availability', '')
        sort_by = request.args.get('sort_by', 'title')

        # Start query
        query = db.session.query(Book)

        # Filter by genre
        if genre:
            query = query.filter(Book.genre == genre)

        # Filter by availability
        if availability == 'available':
            query = query.filter(Book.copies_available > 0)
        elif availability == 'checked-out':
            query = query.filter(Book.copies_available == 0)

        # Sorting
        if sort_by == 'title':
            query = query.order_by(Book.title.asc())
        elif sort_by == 'title-desc':
            query = query.order_by(Book.title.desc())
        elif sort_by == 'author':
            query = query.order_by(Book.author.asc())
        elif sort_by == 'year':
            query = query.order_by(Book.publication_year.desc())
        elif sort_by == 'year-asc':
            query = query.order_by(Book.publication_year.asc())

        all_books = query.all()
        return render_template('books.html', books=all_books, username=current_user.username, genre=genre, availability=availability, sort_by=sort_by)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Books error: {str(e)}")
        print(f"Error details: {error_details}")
        return render_template('books.html', username=current_user.username, error=str(e), error_details=error_details)

@main_bp.route('/members')
@login_required
def members():
    try:
        membership_type = request.args.get('membership_type', '')
        name = request.args.get('name', '')

        query = db.session.query(Member)
        if membership_type:
            query = query.filter(Member.membership_type.ilike(f"%{membership_type}%"))
        if name:
            query = query.filter(Member.name.ilike(f"%{name}%"))

        all_members = query.all()
        return render_template('members.html', members=all_members, username=current_user.username, membership_type=membership_type, name=name)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Members error: {str(e)}")
        print(f"Error details: {error_details}")
        return render_template('members.html', username=current_user.username, error=str(e), error_details=error_details)

@main_bp.route('/loans')
@login_required
def loans():
    try:
        member_id = request.args.get('member_id', '')
        book_id = request.args.get('book_id', '')
        status = request.args.get('status', '')
        today = datetime.now().date()

        query = db.session.query(Loan, Book, Member)\
            .join(Book, Loan.book_id == Book.book_id)\
            .join(Member, Loan.member_id == Member.membership_number)

        if member_id:
            query = query.filter(Loan.member_id == member_id)
        if book_id:
            query = query.filter(Loan.book_id == book_id)
        if status == 'active':
            query = query.filter(Loan.return_date == None, Loan.due_date >= today)
        elif status == 'overdue':
            query = query.filter(Loan.return_date == None, Loan.due_date < today)
        elif status == 'returned':
            query = query.filter(Loan.return_date != None)

        all_loans = query.all()
        return render_template('loans.html', loans=all_loans, username=current_user.username, now=today, member_id=member_id, book_id=book_id, status=status)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Loans error: {str(e)}")
        print(f"Error details: {error_details}")
        return render_template('loans.html', username=current_user.username, error=str(e), error_details=error_details)

@main_bp.route('/reports')
@login_required
def reports():
    return render_template('reports.html', username=current_user.username)

@main_bp.route('/add_book', methods=['POST'])
@login_required
def add_book():
    try:
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publication_year = request.form.get('publication_year')
        copies_available = request.form['copies_available']

        # Generate a unique book_id (you may want to improve this logic)
        import uuid
        book_id = str(uuid.uuid4())[:8]

        new_book = Book(
            book_id=book_id,
            title=title,
            author=author,
            genre=genre,
            publication_year=int(publication_year) if publication_year else None,
            copies_available=int(copies_available)
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('main.books'))
    except Exception as e:
        return render_template('books.html', error="Failed to add book.", error_details=str(e))

@main_bp.route('/add_member', methods=['POST'])
@login_required
def add_member():
    try:
        from uuid import uuid4
        membership_number = str(uuid4())[:8]
        name = request.form['name']
        contact_info = request.form.get('contact_info')
        membership_type = request.form['membership_type']
        join_date = request.form['join_date']
        expiration_date = request.form['expiration_date']

        new_member = Member(
            membership_number=membership_number,
            name=name,
            contact_info=contact_info,
            membership_type=membership_type,
            join_date=join_date,
            expiration_date=expiration_date
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('main.members'))
    except Exception as e:
        return render_template('members.html', error="Failed to add member.", error_details=str(e))

@main_bp.route('/add_loan', methods=['POST'])
@login_required
def add_loan():
    try:
        from uuid import uuid4
        loan_number = str(uuid4())[:8]
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        loan_date = request.form['loan_date']
        due_date = request.form['due_date']

        new_loan = Loan(
            loan_number=loan_number,
            book_id=book_id,
            member_id=member_id,
            loan_date=loan_date,
            due_date=due_date
        )
        db.session.add(new_loan)
        db.session.commit()
        return redirect(url_for('main.loans'))
    except Exception as e:
        return render_template('loans.html', error="Failed to add loan.", error_details=str(e))

@main_bp.route('/edit_member/<membership_number>', methods=['GET', 'POST'])
@login_required
def edit_member(membership_number):
    member = Member.query.filter_by(membership_number=membership_number).first_or_404()
    if request.method == 'POST':
        member.name = request.form['name']
        member.contact_info = request.form['contact_info']
        member.membership_type = request.form['membership_type']
        member.join_date = request.form['join_date']
        member.expiration_date = request.form['expiration_date']
        db.session.commit()
        return redirect(url_for('main.members'))
    return render_template('edit_member.html', member=member, username=current_user.username)

@main_bp.route('/loan_to_member/<membership_number>', methods=['GET', 'POST'])
@login_required
def loan_to_member(membership_number):
    member = Member.query.filter_by(membership_number=membership_number).first_or_404()
    if request.method == 'POST':
        book_id = request.form['book_id']
        loan_date = request.form['loan_date']
        due_date = request.form['due_date']
        from uuid import uuid4
        loan_number = str(uuid4())[:8]
        new_loan = Loan(
            loan_number=loan_number,
            book_id=book_id,
            member_id=membership_number,
            loan_date=loan_date,
            due_date=due_date
        )
        db.session.add(new_loan)
        db.session.commit()
        return redirect(url_for('main.loans'))
    # You may want to pass available books to the template
    books = Book.query.filter(Book.copies_available > 0).all()
    return render_template('loan_to_member.html', member=member, books=books, username=current_user.username)

@main_bp.route('/edit_book/<book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first_or_404()
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.publication_year = request.form.get('publication_year')
        book.copies_available = request.form['copies_available']
        db.session.commit()
        return redirect(url_for('main.books'))
    return render_template('edit_book.html', book=book, username=current_user.username)

@main_bp.route('/loan_book/<book_id>', methods=['GET', 'POST'])
@login_required
def loan_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first_or_404()
    if request.method == 'POST':
        member_id = request.form['member_id']
        loan_date = request.form['loan_date']
        due_date = request.form['due_date']
        from uuid import uuid4
        loan_number = str(uuid4())[:8]
        new_loan = Loan(
            loan_number=loan_number,
            book_id=book_id,
            member_id=member_id,
            loan_date=loan_date,
            due_date=due_date
        )
        db.session.add(new_loan)
        db.session.commit()
        return redirect(url_for('main.loans'))
    members = Member.query.all()
    return render_template('loan_book.html', book=book, members=members, username=current_user.username)

@main_bp.route('/edit_loan/<loan_number>', methods=['GET', 'POST'])
@login_required
def edit_loan(loan_number):
    loan = Loan.query.filter_by(loan_number=loan_number).first_or_404()
    if request.method == 'POST':
        loan.due_date = request.form['due_date']
        loan.return_date = request.form.get('return_date') or None
        db.session.commit()
        return redirect(url_for('main.loans'))
    return render_template('edit_loan.html', loan=loan, username=current_user.username)