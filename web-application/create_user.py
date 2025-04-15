from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load credentials from environment variables (more secure)
load_dotenv()  # Install with: pip install python-dotenv
username = os.getenv('DB_USER', 'root')
password = os.getenv('DB_PASS', 'Meral.2010')
host = os.getenv('DB_HOST', '34.130.33.81')
port = os.getenv('DB_PORT', '3306')
database = os.getenv('DB_NAME', 'backup')  # Change from 'mysql' to your app DB

try:
    # Create a connection to the database
    connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    
    # Ensure the users table exists
    with engine.connect() as connection:
        # Create users table if it doesn't exist
        create_table_query = text("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """)
        connection.execute(create_table_query)
        connection.commit()
        
        # Insert the new user into the users table
        insert_query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        connection.execute(insert_query, {'username': 'admin', 'password': 'admin'})
        connection.commit()
        
    print("User 'admin' created successfully.")
    
except Exception as e:
    print(f"Error: {e}")
