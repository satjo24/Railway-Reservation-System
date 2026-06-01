from tabulate import tabulate
import mysql.connector as mc

# Database connection
try:
    conn = mc.connect(
        host='localhost',
        user='root',
        password='2017',
        port='3307',
        database='r1'
    )
    if conn.is_connected():
        print("✅ CONNECTED TO DATABASE")
except Exception as e:
    print("❌ Database connection error:", e)
    exit()

cur = conn.cursor()

# Create tables safely
cur.execute('''
CREATE TABLE IF NOT EXISTS Trains (
    TRAIN_ID INT PRIMARY KEY,
    TRAIN_NAME VARCHAR(20),
    SOURCE_STATION VARCHAR(20),
    DESTINATION_STATION VARCHAR(20),
    ARRIVAL_TIME VARCHAR(10),
    DEPARTURE_TIME VARCHAR(10),
    CAPACITY INT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Bookings (
    NAME VARCHAR(20),
    AGE INT,
    GENDER VARCHAR(20),
    DISABILITIES VARCHAR(20),
    PHONE_NUMBER VARCHAR(10)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Feedbacks (
    Passenger_Name VARCHAR(20),
    Rating INT,
    Review VARCHAR(50)
)
''')

conn.commit()
print("✅ Tables Created or Exist")

# Admin credentials
admin_credentials = {'b': 'b'}

# Booking Ticket function
def book_ticket():
    try:
        train_id = int(input("Enter the train ID: "))
        cur.execute("SELECT * FROM Trains WHERE TRAIN_ID = %s", (train_id,))
        train_exists = cur.fetchone()

        if not train_exists:
            print("❌ Invalid train ID. Please choose from the available trains.")
            return

        class_selection = input("Enter the class (AC or Non-AC): ")
        num_passengers = int(input("Enter the number of passengers: "))

        if class_selection.upper() == 'AC':
            price_per_passenger = 500
        else:
            price_per_passenger = 300

        total_price = price_per_passenger * num_passengers
        print(f"Total price: {total_price}")

        confirmation = input("Confirm booking (Y/N): ")
        if confirmation.upper() == 'Y':
            for _ in range(num_passengers):
                NAME = input("Enter passenger name: ")
                AGE = int(input("Enter age: "))
                GENDER = input("Enter gender: ")
                DISABILITIES = input("Any disabilities (None if not): ")
                PHONE_NUMBER = input("Enter 10-digit phone number: ")

                if len(PHONE_NUMBER) != 10 or not PHONE_NUMBER.isdigit():
                    print("❌ Invalid phone number. Skipping this passenger.")
                    continue

                cur.execute(
                    "INSERT INTO Bookings (NAME, AGE, GENDER, DISABILITIES, PHONE_NUMBER) VALUES (%s, %s, %s, %s, %s)",
                    (NAME, AGE, GENDER, DISABILITIES, PHONE_NUMBER)
                )
                conn.commit()

            print("✅ Ticket(s) booked successfully. Wishing you a comfortable journey!")
        else:
            print("Booking cancelled.")

    except Exception as e:
        print("❌ Error during booking:", e)

# User authentication
def login(user_type):
    username = input(f"Enter {user_type} username: ")
    password = input(f"Enter {user_type} password: ")
    return username, password

# Main application loop
while True:
    print("\n🎫 Railway Management System 🎫\n")
    print("1. Admin Login")
    print("2. Passenger Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        admin_username, admin_password = login('admin')

        if admin_credentials.get(admin_username) == admin_password:
            print("✅ Admin login successful.")

            while True:
                print("\n🛠️ Admin Menu 🛠️")
                print("1. View Trains")
                print("2. Add Train")
                print("3. Edit Train")
                print("4. Delete Train")
                print("5. View Bookings")
                print("6. View Feedbacks")
                print("7. Logout")

                admin_choice = input("Enter your choice: ")

                if admin_choice == '1':
                    cur.execute("SELECT * FROM Trains")
                    res = cur.fetchall()
                    headers = ['TRAIN_ID', 'TRAIN_NAME', 'SOURCE_STATION', 'DESTINATION_STATION', 'ARRIVAL_TIME', 'DEPARTURE_TIME', 'CAPACITY']
                    print(tabulate(res, headers, tablefmt='outline'))

                elif admin_choice == '2':
                    try:
                        TRAIN_ID = int(input("Enter Train ID: "))
                        TRAIN_NAME = input("Enter Train Name: ")
                        SOURCE_STATION = input("Enter Source Station: ")
                        DESTINATION_STATION = input("Enter Destination Station: ")
                        ARRIVAL_TIME = input("Enter Arrival Time (HH:MM AM/PM): ")
                        DEPARTURE_TIME = input("Enter Departure Time (HH:MM AM/PM): ")
                        CAPACITY = int(input("Enter Train Capacity: "))

                        cur.execute(
                            "INSERT INTO Trains (TRAIN_ID, TRAIN_NAME, SOURCE_STATION, DESTINATION_STATION, ARRIVAL_TIME, DEPARTURE_TIME, CAPACITY) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (TRAIN_ID, TRAIN_NAME, SOURCE_STATION, DESTINATION_STATION, ARRIVAL_TIME, DEPARTURE_TIME, CAPACITY)
                        )
                        conn.commit()
                        print("✅ Train added successfully.")
                    except Exception as e:
                        print("❌ Error adding train:", e)

                elif admin_choice == '3':
                    try:
                        tedit = int(input("Enter Train ID to edit: "))
                        cur.execute("SELECT * FROM Trains WHERE TRAIN_ID = %s", (tedit,))
                        train = cur.fetchone()

                        if train:
                            print(f"Current Train Data: {train}")
                            new_source = input("New Source Station: ")
                            new_arrival = input("New Arrival Time: ")
                            new_destination = input("New Destination Station: ")
                            new_departure = input("New Departure Time: ")

                            cur.execute(
                                "UPDATE Trains SET SOURCE_STATION=%s, ARRIVAL_TIME=%s, DESTINATION_STATION=%s, DEPARTURE_TIME=%s WHERE TRAIN_ID=%s",
                                (new_source, new_arrival, new_destination, new_departure, tedit)
                            )
                            conn.commit()
                            print(f"✅ Train {tedit} updated successfully.")
                        else:
                            print("❌ Train not found.")
                    except Exception as e:
                        print("❌ Error editing train:", e)

                elif admin_choice == '4':
                    try:
                        del_id = int(input("Enter Train ID to delete: "))
                        cur.execute("DELETE FROM Trains WHERE TRAIN_ID = %s", (del_id,))
                        conn.commit()
                        print(f"✅ Train {del_id} deleted successfully.")
                    except Exception as e:
                        print("❌ Error deleting train:", e)

                elif admin_choice == '5':
                    cur.execute("SELECT * FROM Bookings")
                    res = cur.fetchall()
                    headers = ['NAME', 'AGE', 'GENDER', 'DISABILITIES', 'PHONE_NUMBER']
                    print(tabulate(res, headers, tablefmt='outline'))

                elif admin_choice == '6':
                    cur.execute("SELECT * FROM Feedbacks")
                    res = cur.fetchall()
                    headers = ['Passenger Name', 'Rating', 'Review']
                    print(tabulate(res, headers, tablefmt='outline'))

                elif admin_choice == '7':
                    break

                else:
                    print("❌ Invalid choice.")

        else:
            print("❌ Invalid admin credentials.")

    elif choice == '2':
        while True:
            print("\n🚶 Passenger Menu 🚶")
            print("1. View Trains")
            print("2. Book Ticket")
            print("3. Cancel Ticket")
            print("4. Give Feedback")
            print("5. Logout")

            passenger_choice = input("Enter your choice: ")

            if passenger_choice == '1':
                cur.execute("SELECT * FROM Trains")
                res = cur.fetchall()
                headers = ['TRAIN_ID', 'TRAIN_NAME', 'SOURCE', 'DESTINATION', 'ARRIVAL', 'DEPARTURE', 'CAPACITY']
                print(tabulate(res, headers, tablefmt='outline'))

            elif passenger_choice == '2':
                book_ticket()

            elif passenger_choice == '3':
                try:
                    phonenumber = input("Enter passenger phone number to cancel ticket: ")
                    cur.execute("DELETE FROM Bookings WHERE PHONE_NUMBER = %s", (phonenumber,))
                    conn.commit()
                    print("✅ Ticket cancelled successfully.")
                except Exception as e:
                    print("❌ Error cancelling ticket:", e)

            elif passenger_choice == '4':
                try:
                    Name = input("Enter your name: ")
                    Rating = int(input("Rating (1-5): "))
                    Review = input("Write your review: ")

                    cur.execute(
                        "INSERT INTO Feedbacks (Passenger_Name, Rating, Review) VALUES (%s, %s, %s)",
                        (Name, Rating, Review)
                    )
                    conn.commit()

                    responses = {
                        1: "SORRY. We will try to improve our service.",
                        2: "SORRY. We will try to improve our service.",
                        3: "Thank you. For customer support, contact our official website.",
                        4: "Happy to hear from you. Thank you!",
                        5: "Thank you for your valuable feedback!"
                    }
                    print(responses.get(Rating, "Thank you for your feedback."))

                except Exception as e:
                    print("❌ Error submitting feedback:", e)

            elif passenger_choice == '5':
                break

            else:
                print("❌ Invalid choice.")

    elif choice == '3':
        print("👋 Goodbye!")
        break

    else:
        print("❌ Invalid choice. Try again.")

# Close connection
conn.close()
