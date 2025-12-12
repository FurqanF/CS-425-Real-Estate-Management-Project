from db import get_connection

# ------------------- Properties -------------------
def view_properties():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT PropertyID, Type, Address, City, State, Bedrooms, Price, Availability
        FROM Property;
    """)
    rows = cur.fetchall()
    print("\n=== Properties ===")
    for r in rows:
        print(f"ID: {r[0]}, {r[1]} - {r[2]}, {r[3]}, {r[4]} | {r[5]} BR | ${r[6]} | Available: {r[7]}")
    cur.close()
    conn.close()

def show_property_status():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT PropertyID, Type, Availability,
               CASE WHEN EXISTS (SELECT 1 FROM Booking b WHERE b.PropertyID = p.PropertyID) 
                    THEN 'Booked' ELSE 'Not Booked' END AS BookingStatus
        FROM Property p;
    """)
    rows = cur.fetchall()
    print("\n=== Property Status ===")
    for r in rows:
        print(f"ID: {r[0]}, Type: {r[1]}, Available: {r[2]}, Status: {r[3]}")
    cur.close()
    conn.close()

def properties_menu():
    while True:
        print("\n[1] View Properties | [2] Show Property Status | [3] Back to Main Menu")
        choice = input("Select option: ")
        if choice == "1":
            view_properties()
        elif choice == "2":
            show_property_status()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")

# ------------------- Renters -------------------
def view_renters():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT RenterID, UserID, PreferredLocation, Budget, MoveInDate FROM Renter;")
    rows = cur.fetchall()
    print("\n=== Renters ===")
    for r in rows:
        print(f"ID: {r[0]}, User: {r[1]}, Pref: {r[2]}, Budget: {r[3]}, Move-In: {r[4]}")
    cur.close()
    conn.close()

def add_renter():
    name = input("Renter Name: ")
    email = input("Email: ")
    number = input("Phone: ")
    location = input("Location: ")
    pref_loc = input("Preferred Location: ")
    budget = float(input("Budget: "))
    move_in = input("Move-In Date (YYYY-MM-DD): ")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO UserTable (Name, Email, Number, Role, Location)
            VALUES (%s, %s, %s, 'Renter', %s) RETURNING UserID;
        """, (name, email, number, location))
        user_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO Renter (UserID, PreferredLocation, Budget, MoveInDate)
            VALUES (%s, %s, %s, %s);
        """, (user_id, pref_loc, budget, move_in))
        conn.commit()
        print("Renter added successfully!")
    except Exception as e:
        print("Error:", e)
    cur.close()
    conn.close()

def renters_menu():
    while True:
        print("\n[1] View Renters | [2] Add Renter | [3] Back to Main Menu")
        choice = input("Select option: ")
        if choice == "1":
            view_renters()
        elif choice == "2":
            add_renter()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")

# ------------------- Agents -------------------
def add_agent():
    name = input("Agent Name: ")
    email = input("Email: ")
    number = input("Phone: ")
    location = input("Location: ")
    agency = input("Agency Name: ")
    job_title = input("Job Title: ")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO UserTable (Name, Email, Number, Role, Location)
            VALUES (%s, %s, %s, 'Agent', %s) RETURNING UserID;
        """, (name, email, number, location))
        user_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO Agent (UserID, AgencyName, JobTitle)
            VALUES (%s, %s, %s);
        """, (user_id, agency, job_title))
        conn.commit()
        print("Agent added successfully!")
    except Exception as e:
        print("Error:", e)
    cur.close()
    conn.close()

def agents_menu():
    while True:
        print("\n[1] Add Agent | [2] Back to Main Menu")
        choice = input("Select option: ")
        if choice == "1":
            add_agent()
        elif choice == "2":
            break
        else:
            print("Invalid selection.")

# ------------------- Bookings -------------------
def create_booking():
    property_id = input("Property ID: ")
    renter_id = input("Renter ID: ")
    card_number = input("Card Number: ")
    start = input("Start Date (YYYY-MM-DD): ")
    end = input("End Date (YYYY-MM-DD): ")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Booking (PropertyID, RenterID, CardNumber, StartDate, EndDate, TotalCost)
            VALUES (%s, %s, %s, %s, %s,
                (SELECT Price FROM Property WHERE PropertyID=%s)
            );
        """, (property_id, renter_id, card_number, start, end, property_id))
        conn.commit()
        print("Booking created successfully!")
    except Exception as e:
        print("Error:", e)
    cur.close()
    conn.close()

def search_bookings():
    renter_id = input("Enter Renter ID to search bookings (leave blank for all): ")
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT BookingID, PropertyID, RenterID, StartDate, EndDate, TotalCost FROM Booking"
    if renter_id:
        query += " WHERE RenterID = %s"
        cur.execute(query, (renter_id,))
    else:
        cur.execute(query)
    rows = cur.fetchall()
    print("\n=== Bookings ===")
    for r in rows:
        print(f"ID: {r[0]}, Property: {r[1]}, Renter: {r[2]}, {r[3]} to {r[4]}, Total: ${r[5]}")
    cur.close()
    conn.close()

def bookings_menu():
    while True:
        print("\n[1] Create Booking | [2] Search Bookings | [3] Back to Main Menu")
        choice = input("Select option: ")
        if choice == "1":
            create_booking()
        elif choice == "2":
            search_bookings()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")

# ------------------- Payments -------------------
def add_credit_card():
    user_id = input("User ID: ")
    card_number = input("Card Number: ")
    expiry = input("Expiry Date (YYYY-MM-DD): ")
    cvv = input("CVV: ")
    billing_address_id = input("Billing Address ID (optional): ")
    billing_address_id = billing_address_id if billing_address_id else None

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO CreditCard (CardNumber, UserID, BillingAddressID, ExpiryDate, CVV)
            VALUES (%s, %s, %s, %s, %s);
        """, (card_number, user_id, billing_address_id, expiry, cvv))
        conn.commit()
        print("Credit card added successfully!")
    except Exception as e:
        print("Error:", e)
    cur.close()
    conn.close()

def delete_credit_card():
    card_number = input("Enter Card Number to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM CreditCard WHERE CardNumber = %s;", (card_number,))
        conn.commit()
        print("Credit card deleted successfully!")
    except Exception as e:
        print("Error:", e)
    cur.close()
    conn.close()

def payments_menu():
    while True:
        print("\n[1] Add Credit Card | [2] Delete Credit Card | [3] Back to Main Menu")
        choice = input("Select option: ")
        if choice == "1":
            add_credit_card()
        elif choice == "2":
            delete_credit_card()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")

# ------------------- Addresses -------------------
def add_address():
    user_id = input("User ID: ")
    street = input("Street: ")
    city = input("City: ")
    state = input("State: ")
    zipcode = input("ZipCode: ")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Address (UserID, Street, City, State, ZipCode)
            VALUES (%s, %s, %s, %s, %s);
        """, (user_id, street, city, state, zipcode))
        conn.commit()
        print("Address added successfully!")
    except Exception as e:
        print("Error:", e)
    cur.close()
    conn.close()

def delete_address():
    address_id = input("Address ID to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Address WHERE AddressID = %s;", (address_id,))
        conn.commit()
        print("Address deleted successfully!")
    except Exception as e:
        print("Error:", e)
    cur.close()
    conn.close()

def addresses_menu():
    while True:
        print("\n[1] Add Address | [2] Delete Address | [3] Back to Main Menu")
        choice = input("Select option: ")
        if choice == "1":
            add_address()
        elif choice == "2":
            delete_address()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")

# ------------------- Main Menu -------------------
def main_menu():
    while True:
        print("\n=== Real Estate Management System ===")
        print("[1] Properties | [2] Renters | [3] Agents | [4] Bookings | [5] Payments | [6] Addresses | [7] Exit")
        choice = input("Select option: ")

        if choice == "1":
            properties_menu()
        elif choice == "2":
            renters_menu()
        elif choice == "3":
            agents_menu()
        elif choice == "4":
            bookings_menu()
        elif choice == "5":
            payments_menu()
        elif choice == "6":
            addresses_menu()
        elif choice == "7":
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main_menu()