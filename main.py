from db import get_connection

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


def view_renters():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT RenterID, UserID, PreferredLocation, Budget, MoveInDate
        FROM Renter;
    """)
    rows = cur.fetchall()

    print("\n=== Renters ===")
    for r in rows:
        print(f"ID: {r[0]}, User: {r[1]}, Pref: {r[2]}, Budget: {r[3]}, Move-In: {r[4]}")

    cur.close()
    conn.close()


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


def main_menu():
    while True:
        print("\n=== Real Estate Management System ===")
        print("1. View Properties")
        print("2. View Renters")
        print("3. Create Booking")
        print("4. Exit")

        choice = input("Select option: ")

        if choice == "1":
            view_properties()
        elif choice == "2":
            view_renters()
        elif choice == "3":
            create_booking()
        elif choice == "4":
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main_menu()
