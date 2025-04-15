from faker import Faker
import random
import pandas as pd
from book_title_generator import generate_title
from datetime import datetime, timedelta

# Add this function near the top of the file, after importing modules but before generating data
def generate_standard_phone():
    """Generate a phone number in the format '(XXX) XXX-XXXX'"""
    area_code = random.randint(100, 999)
    prefix = random.randint(100, 999)
    line_number = random.randint(1000, 9999)
    return f"({area_code}) {prefix}-{line_number}"

# Initialize Faker instance
fake = Faker()

# Create a fixed set of authors (fewer than the number of books)
author_count = 8000
authors = [fake.name() for _ in range(author_count)]

# Generate data for books
books = []

# Define genres with associated weights (higher weight = more frequent)
genres = [
    'Mystery/Thriller', 'Science Fiction', 'Fantasy', 'Horror', 'Romance', 
    'Literary Fiction', 'Biography & Autobiography', 'Memoir', 'Self-Help', 
    'History', 'Science & Technology', 'Philosophy', 'Politics & Economics', 
    'Business & Finance', 'Psychology', 'Travel & Exploration', 'Poetry', 
    'Graphic Novels & Comics', 'Children Books', 'Cooking'
]

# weights reflecting real-world distribution of book genres
genre_weights = [
    10, 10, 10, 6, 12, 8, 7, 5, 10, 8, 6, 3, 3, 5, 5, 3, 4, 6, 13, 8
]  # Total = 100

# Generate 5000 books using the title generator
for _ in range(5000):
    genre = random.choices(genres, weights=genre_weights, k=1)[0]
    
    books.append({
        'Book ID': fake.isbn13(),
        'Title': generate_title(genre),
        'Author': random.choice(authors),
        'Genre': genre,
        'Publication Year': random.randint(1950, 2022),
        'Copies Available': random.randint(1, 20)
    })

# Generate data for members with join dates and expiration dates
members = []
# Create sets to track used IDs to ensure uniqueness
used_id_numbers = set()
used_membership_numbers = set()

# Set the start date for member registrations to 2020
member_start_date = datetime(2020, 1, 1)

# Define membership types with their durations (in months) and realistic distribution weights
membership_types = {
    'Standard': 12,  # 1 year
    'Student': 8,    # 8 months (academic year)
    'Senior': 24     # 2 years
}
membership_weights = [60, 30, 10]  # 60% Standard, 30% Student, 10% Senior

# Generate more persons to ensure we have around 1000 active memberships
for _ in range(1500):  # Generate 1500 unique persons
    # Generate a unique 5-digit ID Number for the person
    while True:
        id_number = random.randint(10000, 99999)
        if id_number not in used_id_numbers:
            used_id_numbers.add(id_number)
            break
    
    # Create persistent person details that will be the same across all their memberships
    person_name = fake.name()
    contact_info = generate_standard_phone()
    
    # For each person, decide if they have a current active membership (50% chance)
    has_active_membership = random.random() < 0.5
    
    if has_active_membership:
        # Start with a current active membership
        # Expiration date should be in the future
        min_expiration_days = 1  # At least 1 day valid
        max_expiration_days = 365  # At most 1 year valid 
        expiration_date = datetime.now() + timedelta(days=random.randint(min_expiration_days, max_expiration_days))
        
        # Select membership type based on realistic distribution
        membership_type = random.choices(
            list(membership_types.keys()), 
            weights=membership_weights, 
            k=1
        )[0]
        
        # Calculate join date based on membership type and expiration date
        join_date = expiration_date - timedelta(days=30 * membership_types[membership_type])
        
        # Generate unique membership number for this period
        while True:
            membership_number = random.randint(100000, 999999)
            if membership_number not in used_membership_numbers:
                used_membership_numbers.add(membership_number)
                break
        
        # Add the current active membership
        members.append({
            'ID Number': id_number,
            'Membership Number': membership_number,
            'Name': person_name,
            'Contact Info': contact_info,
            'Membership Type': membership_type,
            'Join Date': join_date.strftime('%Y-%m-%d'),
            'Expiration Date': expiration_date.strftime('%Y-%m-%d')
        })
        
        # Start with the current join date for generating previous memberships
        previous_expiration = join_date
    else:
        # This person doesn't have a current active membership
        # Their last membership expired sometime between member_start_date and now
        days_range = (datetime.now() - member_start_date).days
        days_ago = random.randint(1, min(days_range, 365 * 2))  # Expired within the last 2 years
        previous_expiration = datetime.now() - timedelta(days=days_ago)
        
        # Select membership type for their previous membership
        membership_type = random.choices(
            list(membership_types.keys()), 
            weights=membership_weights, 
            k=1
        )[0]
    
    # Now work backwards to generate previous memberships for this person
    # Continue generating previous memberships until we reach the member_start_date
    # or the member randomly doesn't renew
    while previous_expiration > member_start_date:
        # 50% chance the previous membership was a renewal (changed from 80%)
        if random.random() < 0.5:
            # Generate a new membership type for the previous period (10% chance to be different)
            if random.random() < 0.1:
                membership_type = random.choices(
                    list(membership_types.keys()), 
                    weights=membership_weights, 
                    k=1
                )[0]
            
            # Calculate the previous membership's join date
            previous_join = previous_expiration - timedelta(days=30 * membership_types[membership_type])
            
            # If this would be before our start date, stop
            if previous_join < member_start_date:
                break
                
            # Generate unique membership number for this period
            while True:
                membership_number = random.randint(100000, 999999)
                if membership_number not in used_membership_numbers:
                    used_membership_numbers.add(membership_number)
                    break
            
            # Add this previous membership
            members.append({
                'ID Number': id_number,
                'Membership Number': membership_number,
                'Name': person_name,
                'Contact Info': contact_info,
                'Membership Type': membership_type,
                'Join Date': previous_join.strftime('%Y-%m-%d'),
                'Expiration Date': previous_expiration.strftime('%Y-%m-%d')
            })
            
            # Set up for the next iteration
            previous_expiration = previous_join
        else:
            # This member didn't have a previous membership
            break

# Count active members for reporting
current_date_str = datetime.now().strftime('%Y-%m-%d')
active_members = [m for m in members if m['Expiration Date'] >= current_date_str]
print(f"Active members in dataset: {len(active_members)}")
print(f"Total memberships in dataset: {len(members)}")

# Create a dictionary for fast member lookup - use Membership Number as the key
member_dict = {m['Membership Number']: m for m in members}

# Only use active members for loan generation
active_member_ids = [m['Membership Number'] for m in members if m['Expiration Date'] >= current_date_str]

# Initialize loan counter before generating loans
loan_counter = 1

# Generate data for loans with active membership check
loans = []

# Create a dictionary for fast member lookup - use Membership Number as the key
member_dict = {m['Membership Number']: m for m in members}

# Create a dictionary that tracks copies available for each book
book_copies = {book['Book ID']: book['Copies Available'] for book in books}
currently_loaned = {book_id: 0 for book_id in book_copies}

# Set date range for the past few years
start_date = datetime(2020, 1, 1)  # Starting from 5 years ago
end_date = datetime.now()

# Generate loans day by day from start_date to end_date
current_date = start_date
while current_date <= end_date:
    # Generate 3-10 loans for this day
    loans_today = random.randint(3, 10)
    loans_added = 0
    
    # Try adding loans_today loans for this day
    for _ in range(loans_today * 3):  # We'll try 3 times more than needed to ensure enough valid loans
        if loans_added >= loans_today:
            break
            
        # Pick a random book and member
        book_id = random.choice([book['Book ID'] for book in books])
        member_id = random.choice([member['Membership Number'] for member in members])
        
        # Check if membership was active on loan date
        member = member_dict[member_id]
        member_join_date = datetime.strptime(member['Join Date'], '%Y-%m-%d')
        member_expiration = datetime.strptime(member['Expiration Date'], '%Y-%m-%d')
        
        if not (member_join_date <= current_date <= member_expiration):
            continue  # Skip this loan, membership wasn't active
        
        # First, handle returns that might have happened on this date
        for existing_loan in loans:
            if (existing_loan['Book ID'] == book_id and 
                existing_loan['Return Date'] is not None and
                datetime.strptime(existing_loan['Return Date'], '%Y-%m-%d').date() == current_date.date()):
                # This book was returned on the current date
                currently_loaned[book_id] -= 1
        
        # Check if we have copies available to loan
        if currently_loaned[book_id] < book_copies[book_id]:
            # We can loan this book!
            currently_loaned[book_id] += 1
            
            # Set loan date to current date
            loan_date = current_date
            
            # Due date is typically 2-4 weeks after loan date
            loan_period_days = random.randint(14, 28)
            due_date = loan_date + timedelta(days=loan_period_days)
            
            # Set grace period to 30 days after due date
            grace_period = 30
            grace_date = due_date + timedelta(days=grace_period)
            
            # Determine if the book was returned based on dates
            # Updated behavior: Only 3% of books remain unreturned after grace period
            if grace_date < end_date:
                # This book's grace period is in the past
                is_returned = random.choices([True, False], weights=[97, 3], k=1)[0]  # 97% returned, 3% unreturned
            elif due_date < end_date:
                # Due date passed but still in grace period
                is_returned = random.choices([True, False], weights=[70, 30], k=1)[0]  # 70% returned
            else:
                # Still within loan period
                is_returned = random.choices([True, False], weights=[30, 70], k=1)[0]  # 30% returned
            
            # For returned books, return date is between loan date and either due date + some grace period or today
            if is_returned:
                # Most people return around the due date (before, on, or shortly after)
                days_around_due = random.choices(
                    [
                        # Early return (before due date)
                        random.randint(1, max(1, (due_date - loan_date).days - 1)),
                        # On-time return (right around due date)
                        (due_date - loan_date).days + random.randint(0, 3),
                        # Late return (within grace period)
                        (due_date - loan_date).days + random.randint(4, grace_period)
                    ], 
                    weights=[20, 60, 20],  # Most returns happen right around the due date
                    k=1
                )[0]
                
                return_date = loan_date + timedelta(days=days_around_due)
                
                # Make sure return date isn't in the future
                if return_date > end_date:
                    return_date = end_date
                
                return_date_str = return_date.strftime('%Y-%m-%d')
            else:
                return_date_str = None
            
            loans.append({
                'Loan Number': f'{loan_counter:05d}',  # Format as 5 digits with leading zeros
                'Book ID': book_id,
                'Member ID': member_id,
                'Loan Date': loan_date.strftime('%Y-%m-%d'),
                'Due Date': due_date.strftime('%Y-%m-%d'),
                'Return Date': return_date_str
            })
            
            # Increment loan counter for next loan
            loan_counter += 1
            
            loans_added += 1
    
    # Move to the next day
    current_date += timedelta(days=1)

print(f"Total loans generated: {len(loans)}")

# Convert dates to strings only when creating the DataFrame
for loan in loans:
    loan['Loan Date'] = loan['Loan Date']
    loan['Due Date'] = loan['Due Date']
    if loan['Return Date'] is not None:
        loan['Return Date'] = loan['Return Date']

# Create DataFrames for each table
books_df = pd.DataFrame(books)
members_df = pd.DataFrame(members)
loans_df = pd.DataFrame(loans)

# Display sample data
print("Books DataFrame:")
print(books_df.head())
print("\nMembers DataFrame:")
print(members_df.head())
print("\nLoans DataFrame:")
print(loans_df.head())

# Save DataFrames to CSV files
books_df.to_csv('books.csv', index=False)
members_df.to_csv('members.csv', index=False)
loans_df.to_csv('loans.csv', index=False)