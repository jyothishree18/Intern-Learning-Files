import json

FILE_NAME = "contacts.json"


def load_contacts():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_contacts():
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)


contacts = load_contacts()


def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    contacts[name] = phone
    save_contacts()
    print("Contact added!")


def list_contacts():
    if not contacts:
        print("No contacts found.")
        return

    for name, phone in contacts.items():
        print(name, "-", phone)


def find_contact():
    name = input("Enter name to find: ").strip()

    if name in contacts:
        print(name, "-", contacts[name])
    else:
        print("Contact not found.")


def delete_contact():
    name = input("Enter name to delete: ").strip()

    if name in contacts:
        del contacts[name]
        save_contacts()
        print("Contact deleted!")
    else:
        print("Contact not found.")


def main():
    while True:
        print("\n--- Contact Book ---")
        print("1. Add")
        print("2. List")
        print("3. Find")
        print("4. Delete")
        print("5. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            list_contacts()
        elif choice == "3":
            find_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
