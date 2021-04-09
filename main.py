from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    # Retrieves user inputs from app and stores them to new_data
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # Check to see if user left any fields empty
    if website == "" or email == "" or password == "":
        messagebox.showwarning(title="Oops!", message="Please do not leave any fields empty!")
    else:
        # Try to open the file in read mode and store the info into a variable called data
        try:
            with open("password_file.json", "r") as data_file:
                data = json.load(data_file)
    # If the file doesn't exist, catch that error and create a new file, write our new_data to that file
        except FileNotFoundError:
            with open("password_file.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
    # If there were no errors in the try block, update the data variable with our new data
        else:
            data.update(new_data)
    # Use that updated data variable to write in the data_file
            with open("password_file.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
    # Clear the contents from the input boxes
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH ------------------------------- #


def find_password():
    website = website_entry.get()
    # Check to see if the data file has any information
    try:
        with open("password_file.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # Pop up that there is no password saved for this website
        messagebox.showwarning(title="Error", message="No data file found.")
    else:
        # Check to see if the specific website has been uploaded into the data file
        if website in data:
            searched_email = data[website]["email"]
            searched_password = data[website]["password"]
            messagebox.showinfo(website, message=f"Email/Username: {searched_email}\n"
                                                 f"Password: {searched_password}\n"
                                                 f"Password copied to clipboard.")
            pyperclip.copy(searched_password)

        else:
            # Pop up that there is no password saved for this website
            messagebox.showwarning(title="Oops!", message="There is no information about this website stored here.")

    # Clear the contents from the input boxes
    finally:
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

pass_gen_button = Button(text="Generate Password", command=gen_password)
pass_gen_button.grid(column=2, row=3)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)

add_button = Button(text="Add", width=45, command=save)
add_button.grid(column=1, row=4, columnspan=2)

website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_entry = Entry(width=53)
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

window.mainloop()
