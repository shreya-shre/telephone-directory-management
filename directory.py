import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
import os

# Connect to the MySQL server
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin123",
    database="my_databse"
)

# Create a cursor object
cursor = cnx.cursor()

# Define a function for adding a new contact
def add_contact():
    name = entry_name.get()
    phone_number = entry_phone_number.get()
    email = entry_email.get()
    address = entry_address.get()

    if not name or not phone_number:
        messagebox.showerror("Error", "Name and phone number are required.")
        return

    query = "INSERT INTO contacts (name, phone_number, email, address) VALUES (%s, %s, %s, %s)"
    values = (name, phone_number, email, address)
    cursor.execute(query, values)
    cnx.commit()

    clear_fields()
    view_contacts()

# Define a function for viewing all contacts
def view_contacts():
    query = "SELECT * FROM contacts"
    cursor.execute(query)
    result = cursor.fetchall()

    tree_contacts.delete(*tree_contacts.get_children())
    for row in result:
        tree_contacts.insert("", "end", values=row)

# Define a function for clearing all fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_phone_number.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

# Define a function for deleting a contact
def delete_contact():
    selected_item = tree_contacts.selection()
    if selected_item:
        contact_id = tree_contacts.item(selected_item, 'values')[0]
        query = "DELETE FROM contacts WHERE id = %s"
        cursor.execute(query, (contact_id,))
        cnx.commit()
        view_contacts()

# Define a function for updating a contact
def update_contact():
    selected_item = tree_contacts.selection()
    if selected_item:
        contact_id = tree_contacts.item(selected_item, 'values')[0]
        name = entry_name.get()
        phone_number = entry_phone_number.get()
        email = entry_email.get()
        address = entry_address.get()

        if not name or not phone_number:
            messagebox.showerror("Error", "Name and phone number are required.")
            return

        query = "UPDATE contacts SET name = %s, phone_number = %s, email = %s, address = %s WHERE id = %s"
        values = (name, phone_number, email, address, contact_id)
        cursor.execute(query, values)
        cnx.commit()
        view_contacts()

# Define a function for calling a contact
def call_contact():
    selected_item = tree_contacts.selection()
    if selected_item:
        phone_number = tree_contacts.item(selected_item, 'values')[2]
        # Use the 'start' command followed by the phone number to initiate a call
        os.system(f'start tel:{phone_number}')

# Define a function for sending an email to a contact
def send_email():
    selected_item = tree_contacts.selection()
    if selected_item:
        email_address = tree_contacts.item(selected_item, 'values')[3]
        os.system(f'start mailto:{email_address}')
        
# Create the main window
window_main = tk.Tk()
window_main.title("Contact Book")

# Create labels and entry fields for adding a new contact
label_name = tk.Label(window_main, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_name = tk.Entry(window_main)
entry_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

label_phone_number = tk.Label(window_main, text="Phone Number:")
label_phone_number.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_phone_number = tk.Entry(window_main)
entry_phone_number.grid(row=1, column=1, padx=10, pady=10, sticky="w")

label_email = tk.Label(window_main, text="Email:")
label_email.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_email = tk.Entry(window_main)
entry_email.grid(row=2, column=1, padx=10, pady=10, sticky="w")

label_address = tk.Label(window_main, text="Address:")
label_address.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_address = tk.Entry(window_main)
entry_address.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Create buttons for adding, updating, deleting, calling, and sending email to contacts
button_add_contact = tk.Button(window_main, text="Add Contact", command=add_contact)
button_add_contact.grid(row=4, column=0, padx=10, pady=10, sticky="w")

button_update_contact = tk.Button(window_main, text="Update Contact", command=update_contact)
button_update_contact.grid(row=4, column=1, padx=10, pady=10, sticky="w")

button_delete_contact = tk.Button(window_main, text="Delete Contact", command=delete_contact)
button_delete_contact.grid(row=4, column=2, padx=10, pady=10, sticky="w")

button_call_contact = tk.Button(window_main, text="Call", command=call_contact)
button_call_contact.grid(row=4, column=3, padx=10, pady=10, sticky="w")

button_send_email = tk.Button(window_main, text="Send Email", command=send_email)
button_send_email.grid(row=4, column=4, padx=10, pady=10, sticky="w")

# Create a tree view for displaying all contacts
tree_contacts = ttk.Treeview(window_main)
tree_contacts["columns"] = ("id", "name", "phone_number", "email", "address")
tree_contacts.heading("#0", text="")
tree_contacts.heading("id", text="ID")
tree_contacts.heading("name", text="Name")
tree_contacts.heading("phone_number", text="Phone Number")
tree_contacts.heading("email", text="Email")
tree_contacts.heading("address", text="Address")
tree_contacts.column("#0", width=0)
tree_contacts.column("id", width=50)
tree_contacts.column("name", width=150)
tree_contacts.column("phone_number", width=150)
tree_contacts.column("email", width=200)
tree_contacts.column("address", width=200)
tree_contacts.grid(row=5, columnspan=5, padx=10, pady=10)

# Call view_contacts() to display contacts when the application starts
view_contacts()

# Start the Tkinter event loop
window_main.mainloop()

# Close the cursor and connection
cursor.close()
cnx.close()
