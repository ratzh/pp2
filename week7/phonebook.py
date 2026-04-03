import csv
from connect import get_connection

# Create table
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table is ready.")


# Insert contacts from CSV
def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted.")


# Manual insertion
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact inserted from console.")


# Update contact
def update_contact():
    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")


# Search contacts
def query_contacts():
    choice = input("Search by (1-name / 2-phone prefix): ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
    elif choice == "2":
        prefix = input("Enter phone prefix: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + "%",))

    rows = cur.fetchall()

    if rows:
        print("ID | Name                | Phone")
        print("-------------------------------")
        for row in rows:
            print(f"{row[0]:<2} | {row[1]:<18} | {row[2]}")
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


# Delete contact
def delete_contact():
    choice = input("Delete by (1-name / 2-phone / 3-all): ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        print("Contact deleted.")
    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        print("Contact deleted.")
    elif choice == "3":
        # Delete all contacts and reset ID
        cur.execute("TRUNCATE TABLE phonebook RESTART IDENTITY;")
        print("All contacts deleted and IDs reset.")

    conn.commit()
    cur.close()
    conn.close()


# Show all contacts
def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()

    if rows:
        print("ID | Name                | Phone")
        print("-------------------------------")
        for row in rows:
            print(f"{row[0]:<2} | {row[1]:<18} | {row[2]}")
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


# Menu
def menu():
    while True:
        print("""
1. Create table
2. Insert from CSV
3. Insert from console
4. Update contact
5. Query contacts
6. Delete contact
7. Show all contacts
8. Exit
        """)

        choice = input("Choose an option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            show_all_contacts()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()