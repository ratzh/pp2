from connect import connect
import csv


def insert_contact(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact_2(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()


def search_contact(value):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts_2(%s)", (value,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()


def get_paginated(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated_2(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_contact(value):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact_2(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()


def insert_many():
    print("Enter multiple contacts. Leave name empty to finish.")

    names = []
    phones = []

    while True:
        name = input("Name: ").strip()
        if not name:  # бос қалдырса, енгізуді аяқтау
            break
        phone = input("Phone (11 digits): ").strip()
        names.append(name)
        phones.append(phone)

    if not names:
        print("No contacts entered.")
        return

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "CALL insert_many_contacts_2(%s::text[], %s::text[])",
        (names, phones)
    )
    conn.commit()
    cur.close()
    conn.close()

    print(f"{len(names)} contacts inserted successfully!")


def insert_from_csv(file):
    conn = connect()
    cur = conn.cursor()
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        names, phones = [], []
        for row in reader:
            names.append(row[0])
            phones.append(row[1])
    cur.execute("CALL insert_many_contacts_2(%s, %s)", (names, phones))
    conn.commit()
    cur.close()
    conn.close()


while True:
    print("\n1. Add contact")
    print("2. Search (name or phone)")
    print("3. Pagination")
    print("4. Delete (name or phone)")
    print("5. Bulk insert example")
    print("6. Import CSV")
    print("7. Exit")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        insert_contact(name, phone)

    elif choice == "2":
        value = input("Enter name or phone: ")
        search_contact(value)

    elif choice == "3":
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        get_paginated(limit, offset)

    elif choice == "4":
        value = input("Enter name or phone: ")
        delete_contact(value)

    elif choice == "5":
        insert_many()

    elif choice == "6":
        file = input("Enter CSV file path: ")
        insert_from_csv(file)

    elif choice == "7":
        break

    else:
        print("Invalid choice, try again.")