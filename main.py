from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# Constants
DATA_FILE = "data.json"
LOGO_FILE = "logo.png"


def search_data():
    web_search = web_entry.get()

    try:
        with open(DATA_FILE, "r") as data_file:
            data = json.load(data_file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        messagebox.showinfo(title="Warning", message="No record found!")
    else:
        if web_search in data:
            email = data[web_search]["email"]
            password = data[web_search]["password"]
            pyperclip.copy(password)
            message = f"Email: {email}\nPassword: {password}"
            messagebox.showinfo(title="Information", message=message)
        else:
            messagebox.showinfo(title="Warning", message="No record found")


def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    pass_entry.delete(0, END)
    pass_entry.insert(0, password)
    pyperclip.copy(password)


def save_data():
    web_data = web_entry.get()
    email_data = email_entry.get()
    pass_data = pass_entry.get()

    new_data = {
        web_data: {
            "email": email_data,
            "password": pass_data
        }
    }

    confirmation_message = (
        f"The details entered: \nEmail: {email_data}\nPassword: {pass_data} \nIs it ok to save?"
    )

    if not web_data or not pass_data:
        messagebox.showinfo(title="Warning", message="Please don't leave any fields empty!")
    else:
        user_confirmed = messagebox.askokcancel(title="Website", message=confirmation_message)
        if user_confirmed:
            try:
                with open(DATA_FILE, "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
                    # Updating old data with new data
                    data.update(new_data)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open(DATA_FILE, "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                with open(DATA_FILE, "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                web_entry.delete(0, END)
                pass_entry.delete(0, END)


# UI Setup
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

photo = PhotoImage(file=LOGO_FILE)
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=photo)

web_label = Label(text="Website:")
email_label = Label(text="Email/Username:")
pass_label = Label(text="Password")

web_entry = Entry(width=21)
web_entry.focus()
email_entry = Entry(width=35)
email_entry.insert(0, "nikhiltelase@gmail.com")
pass_entry = Entry(width=21, show="*")

search_button = Button(text="Search", command=search_data, width=13)
gen_pass_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", width=36, command=save_data)

canvas.grid(column=1, row=0)
web_label.grid(column=0, row=1)
web_entry.grid(column=1, row=1, ipadx=45)
search_button.grid(column=2, row=1)
email_label.grid(column=0, row=2)
email_entry.grid(column=1, row=2, columnspan=2, ipadx=55)
pass_label.grid(column=0, row=3)
pass_entry.grid(column=1, row=3, ipadx=42)
gen_pass_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2, ipadx=32)

window.mainloop()
