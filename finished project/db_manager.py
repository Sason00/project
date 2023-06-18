import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Establish a connection to the database file
conn = sqlite3.connect('') # name of db file
cursor = conn.cursor()

# Function to fetch data from a table and display it in a tab
def fetch_table_data(tab, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    table_frame = Frame(tab)
    table_frame.pack(fill='both', expand=True)

    # Create a treeview to display the table data
    treeview = ttk.Treeview(table_frame, columns=list(range(len(rows[0]))), show="headings")
    treeview.pack(side='left', fill='both', expand=True)

    # Set the column headings based on the table columns
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    for col in columns:
        treeview.heading(col[0], text=col[1])

    # Insert the table data into the treeview
    for row in rows:
        treeview.insert("", "end", values=row)


# Function to add a user to the database
def add_user(username, password, email, user_type):
    try:
        cursor.execute('''INSERT INTO users (username, password, email, type)
                        VALUES (?, ?, ?, ?)''', (username, password, email, user_type))
        conn.commit()
        messagebox.showinfo('Success', 'User added successfully!')
    except sqlite3.Error as error:
        messagebox.showerror('Error', str(error))

# Function to delete a user from the database
def delete_user(user_id):
    try:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        messagebox.showinfo('Success', 'User deleted successfully!')
    except sqlite3.Error as error:
        messagebox.showerror('Error', str(error))

# Function to add an active room to the database
def add_active_room(room_code, host_id, host_ip=None, host_port=None, host_listener_port=None):
    try:
        cursor.execute('''INSERT INTO active_rooms (room_code, host_id, host_ip, host_port, host_listener_port)
                        VALUES (?, ?, ?, ?, ?)''', (room_code, host_id, host_ip, host_port, host_listener_port))
        conn.commit()
        messagebox.showinfo('Success', 'Active room added successfully!')
    except sqlite3.Error as error:
        messagebox.showerror('Error', str(error))

# Function to delete an active room from the database
def delete_active_room(room_code):
    try:
        cursor.execute('DELETE FROM active_rooms WHERE room_code = ?', (room_code,))
        conn.commit()
        messagebox.showinfo('Success', 'Active room deleted successfully!')
    except sqlite3.Error as error:
        messagebox.showerror('Error', str(error))

# Function to view the users and active_rooms tables
def view_tables():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    print("Users:")
    for user in users:
        print(user)

    cursor.execute('SELECT * FROM active_rooms')
    active_rooms = cursor.fetchall()
    print("Active Rooms:")
    for room in active_rooms:
        print(room)

# GUI Function to add a user
def add_user_gui():
    def add_user_button():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        user_type = type_entry.get()
        add_user(username, password, email, user_type)
        add_user_window.destroy()

    add_user_window = Tk()
    add_user_window.title('Add User')

    username_label = Label(add_user_window, text='Username:')
    username_label.pack()
    username_entry = Entry(add_user_window)
    username_entry.pack()

    password_label = Label(add_user_window, text='Password:')
    password_label.pack()
    password_entry = Entry(add_user_window)
    password_entry.pack()

    email_label = Label(add_user_window, text='Email:')
    email_label.pack()
    email_entry = Entry(add_user_window)
    email_entry.pack()

    type_label = Label(add_user_window, text='Type:')
    type_label.pack()
    type_entry = Entry(add_user_window)
    type_entry.pack()

    add_button = Button(add_user_window, text='Add User', command=add_user_button)
    add_button.pack()

    add_user_window.mainloop()

# GUI Function to delete a user
def delete_user_gui():
    def delete_user_button():
        user_id = user_id_entry.get()
        delete_user(user_id)
        delete_user_window.destroy()

    delete_user_window = Tk()
    delete_user_window.title('Delete User')

    user_id_label = Label(delete_user_window, text='User ID:')
    user_id_label.pack()
    user_id_entry = Entry(delete_user_window)
    user_id_entry.pack()

    delete_button = Button(delete_user_window, text='Delete User', command=delete_user_button)
    delete_button.pack()

    delete_user_window.mainloop()

# GUI Function to add an active room
def add_active_room_gui():
    def add_active_room_button():
        room_code = room_code_entry.get()
        host_id = host_id_entry.get()
        host_ip = host_ip_entry.get()
        host_port = host_port_entry.get()
        host_listener_port = host_listener_port_entry.get()
        add_active_room(room_code, host_id, host_ip, host_port, host_listener_port)
        add_active_room_window.destroy()

    add_active_room_window = Tk()
    add_active_room_window.title('Add Active Room')

    room_code_label = Label(add_active_room_window, text='Room Code:')
    room_code_label.pack()
    room_code_entry = Entry(add_active_room_window)
    room_code_entry.pack()

    host_id_label = Label(add_active_room_window, text='Host ID:')
    host_id_label.pack()
    host_id_entry = Entry(add_active_room_window)
    host_id_entry.pack()

    host_ip_label = Label(add_active_room_window, text='Host IP:')
    host_ip_label.pack()
    host_ip_entry = Entry(add_active_room_window)
    host_ip_entry.pack()

    host_port_label = Label(add_active_room_window, text='Host Port:')
    host_port_label.pack()
    host_port_entry = Entry(add_active_room_window)
    host_port_entry.pack()

    host_listener_port_label = Label(add_active_room_window, text='Host Listener Port:')
    host_listener_port_label.pack()
    host_listener_port_entry = Entry(add_active_room_window)
    host_listener_port_entry.pack()

    add_button = Button(add_active_room_window, text='Add Active Room', command=add_active_room_button)
    add_button.pack()

    add_active_room_window.mainloop()

# GUI Function to delete an active room
def delete_active_room_gui():
    def delete_active_room_button():
        room_code = room_code_entry.get()
        delete_active_room(room_code)
        delete_active_room_window.destroy()

    delete_active_room_window = Tk()
    delete_active_room_window.title('Delete Active Room')

    room_code_label = Label(delete_active_room_window, text='Room Code:')
    room_code_label.pack()
    room_code_entry = Entry(delete_active_room_window)
    room_code_entry.pack()

    delete_button = Button(delete_active_room_window, text='Delete Active Room', command=delete_active_room_button)
    delete_button.pack()

    delete_active_room_window.mainloop()

# GUI Function to view the tables
def view_tables_gui():
    view_tables()
    messagebox.showinfo('Tables', 'Tables printed in the console.')



# Main GUI window
main_window = Tk()
main_window.title('Database Management')


# Create a notebook (tabs) to display tables
notebook = ttk.Notebook(main_window)
notebook.pack(fill='both', expand=True)

# Get the table names from the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

# Create a tab for each table
for table in tables:
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=table[0])
    fetch_table_data(tab, table[0])

# Buttons to perform actions
add_user_button = Button(main_window, text='Add User', command=add_user_gui)
add_user_button.pack()

delete_user_button = Button(main_window, text='Delete User', command=delete_user_gui)
delete_user_button.pack()

add_active_room_button = Button(main_window, text='Add Active Room', command=add_active_room_gui)
add_active_room_button.pack()

delete_active_room_button = Button(main_window, text='Delete Active Room', command=delete_active_room_gui)
delete_active_room_button.pack()

view_tables_button = Button(main_window, text='View Tables', command=view_tables_gui)
view_tables_button.pack()

main_window.mainloop()

# Close the connection to the database
conn.close()

