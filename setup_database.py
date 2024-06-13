# setup_database.py

from Files.myDatabase import conn, cursor
from Files.user import User  
from Files.organization import Organization  
from Files.address import Address  

def setup_database():
    User.create_table()
    Organization.create_table()
    Address.create_table()
    print("All tables created successfully.")

if __name__ == "__main__":
    setup_database()
