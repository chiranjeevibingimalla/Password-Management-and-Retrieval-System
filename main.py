from tkinter import *
from tkinter import messagebox
import random
import json
import pyperclip

FONT = ("Times New Roman", 13, "normal")
BUTTON_FONT = ("Times New Roman", 10, "normal")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_numbers + password_symbols + password_letters
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    print(f"Your password is: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def clear_text():
    website_entry.delete(0, END)
    password_entry.delete(0, END)


def add_password():
    website_name = (website_var.get()).title()
    username = username_var.get()
    password = password_var.get()
    new_data = {
        website_name: {
            "email": username,
            "password": password
        }
    }
    if len(website_name) == 0 or len(password) == 0 or len(username) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            clear_text()


# ------------------------ SEARCH WEBSITE ----------------------------- #


def find_password():
    website_name = (website_var.get()).strip().title()
    try:
        with open("data.json", "r") as password_file:
            password_data = json.load(password_file)
            email_username = password_data[website_name]["email"]
            website_pass = password_data[website_name]["password"]
            pyperclip.copy(website_pass)
            messagebox.showinfo(title="Credentials", message=f"Username: {email_username} \nPassword: {website_pass} ")
            
    except FileNotFoundError:
        print(f"Sorry,there is no file")
    except KeyError as error_name:
        messagebox.showerror(title="Error", message=f"Login credentials of {error_name} are not found")
        print(f"Login credentials of {error_name} are not present\n")




# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

website_var = StringVar()
username_var = StringVar()
password_var = StringVar()

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
username_label = Label(text="Email/Username:")
password_label = Label(text="Password:")
# Entries
website_entry = Entry(width=17, textvariable=website_var)
website_entry.focus()
username_entry = Entry(width=35, textvariable=username_var)
username_entry.insert(0, "bingimalla4@gmail.com")
password_entry = Entry(width=17, textvariable=password_var)
# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", width=30, command=add_password)
search_button = Button(text="Search", width=15, command=find_password)
# Grid
website_label.grid(column=0, row=1)
username_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)

website_entry.grid(column=1, row=1)
username_entry.grid(column=1, columnspan=2, row=2)
password_entry.grid(column=1, row=3)

generate_password_button.grid(column=2, row=3)
add_button.grid(column=1, columnspan=2, row=4)
search_button.grid(column=2, row=1)

window.mainloop()
