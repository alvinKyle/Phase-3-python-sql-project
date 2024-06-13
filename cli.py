import sys
from Files.user import User
from Files.organization import Organization
from Files.address import Address

def setup_database():
    User.create_table()
    Organization.create_table()
    Address.create_table()
    print("All tables created successfully.")

def display_menu():
    print("""
    Welcome to Tuwapange Managing System
    1. Add Contact
    2. Update Contact
    3. Delete Contact
    4. View Contacts
    5. Add Organization
    6. Update Organization
    7. Delete Organization
    8. View Organizations
    9. Add Address
    10. Update Address
    11. Delete Address
    12. View Addresses
    0. Exit
    """)

def main():
    setup_database()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        try:
            if choice == '1':
                username = input("Enter username: ")
                phone_no = int(input("Enter phone number: "))
                email = input("Enter email: ")
                org_id = int(input("Enter organization ID (optional, press Enter to skip): ") or 0)
                User.create(username, phone_no, email, org_id if org_id else None)
                print("User added successfully.")
            
            elif choice == '2':
                contact_id = int(input("Enter User ID to update: "))
                contact = User.find_by_id(contact_id)
                if contact:
                    contact.username = input("Enter new username: ")
                    contact.phone_no = int(input("Enter new phone number: "))
                    contact.email = input("Enter new email: ")
                    org_id = int(input("Enter new organization ID (optional, press Enter to skip): ") or 0)
                    contact.org_id = org_id if org_id else None
                    contact.update()
                    print("Contact updated successfully.")
                else:
                    print("Contact not found.")
            
            elif choice == '3':
                contact_id = int(input("Enter contact ID to delete: "))
                contact = User.find_by_id(contact_id)
                if contact:
                    contact.delete()
                    print("Contact deleted successfully.")
                else:
                    print("Contact not found.")
            
            elif choice == '4':
                contacts = User.get_all()
                for contact in contacts:
                    print(contact)
            
            elif choice == '5':
                name = input("Enter organization name: ")
                Organization.create(name)
                print("Organization added successfully.")
            
            elif choice == '6':
                org_id = int(input("Enter organization ID to update: "))
                organization = Organization.find_by_id(org_id)
                if organization:
                    organization.name = input("Enter new organization name: ")
                    organization.update()
                    print("Organization updated successfully.")
                else:
                    print("Organization not found.")
            
            elif choice == '7':
                org_id = int(input("Enter organization ID to delete: "))
                organization = Organization.find_by_id(org_id)
                if organization:
                    organization.delete()
                    print("Organization deleted successfully.")
                else:
                    print("Organization not found.")
            
            elif choice == '8':
                organizations = Organization.get_all()
                for organization in organizations:
                    print(organization)
            
            elif choice == '9':
                country = input("Enter country: ")
                city = input("Enter city: ")
                user_id = int(input("Enter user ID: "))
                org_id = int(input("Enter organization ID: "))
                Address.create(country, city, user_id, org_id)
                print("Address added successfully.")
            
            elif choice == '10':
                address_id = int(input("Enter address ID to update: "))
                address = Address.find_by_id(address_id)
                if address:
                    address.country = input("Enter new country: ")
                    address.city = input("Enter new city: ")
                    address.user_id = int(input("Enter new user ID: "))
                    address.org_id = int(input("Enter new organization ID: "))
                    address.update()
                    print("Address updated successfully.")
                else:
                    print("Address not found.")
            
            elif choice == '11':
                address_id = int(input("Enter address ID to delete: "))
                address = Address.find_by_id(address_id)
                if address:
                    address.delete()
                    print("Address deleted successfully.")
                else:
                    print("Address not found.")
            
            elif choice == '12':
                addresses = Address.get_all()
                for address in addresses:
                    print(address)
            
            elif choice == '0':
                print("Exited")
                sys.exit()
            
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
